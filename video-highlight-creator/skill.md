---
name: video-highlight-creator
description: Automatically create short highlight clips from long-form videos using AI-powered scene detection, speech-to-text analysis, and intelligent scoring. Transforms 30-60 min raw videos into engaging 60-90 second highlight reels with professional editing. Uses FFmpeg for scene detection, AssemblyAI for transcription, custom scoring algorithms, and Remotion for final rendering.
---

# Video Highlight Creator

Transform long-form videos (30-60 minutes) into engaging short clips (60-90 seconds) using AI-powered analysis and intelligent scoring.

## Trigger

Activate when user says:
- "create video highlights"
- "extract best moments from video"
- "turn long video into short clip"
- "auto-edit video highlights"
- "find best clips in video"

## Prerequisites

### Required Tools
1. **FFmpeg** - Scene detection, audio extraction, video processing
2. **AssemblyAI API** - Speech-to-text transcription and sentiment analysis
3. **Remotion** - Final video rendering and assembly
4. **Node.js** - Script execution

### API Keys Required
```bash
# AssemblyAI API Key
# Get free tier: https://www.assemblyai.com/
# Free tier: 3 hours of audio per month
ASSEMBLYAI_API_KEY=your_key_here
```

### Installation
```bash
# Install FFmpeg (if not already installed)
# Windows: Download from https://ffmpeg.org/download.html
# Mac: brew install ffmpeg
# Linux: apt-get install ffmpeg

# Install Node dependencies
npm install @remotion/bundler @remotion/cli react react-dom remotion
npm install assemblyai axios fluent-ffmpeg
```

## Core Workflow

**Pipeline Overview:**
```
Raw Video (60 min)
    ↓
[1] Scene Detection (FFmpeg)
    ↓
[2] Audio Extraction & Transcription (AssemblyAI)
    ↓
[3] Segment Scoring (Custom Algorithm)
    ↓
[4] Clip Selection (Top N segments)
    ↓
[5] Remotion Assembly & Render
    ↓
Final Highlight Reel (60-90s)
```

---

## Step 1: Scene Detection with FFmpeg

Analyze video for scene changes, motion intensity, and audio peaks.

### 1A: Extract Video Metadata

```javascript
// analyze-video.js
const ffmpeg = require('fluent-ffmpeg');
const { promisify } = require('util');
const exec = promisify(require('child_process').exec);

async function getVideoMetadata(videoPath) {
  return new Promise((resolve, reject) => {
    ffmpeg.ffprobe(videoPath, (err, metadata) => {
      if (err) reject(err);
      const videoStream = metadata.streams.find(s => s.codec_type === 'video');
      const audioStream = metadata.streams.find(s => s.codec_type === 'audio');

      resolve({
        duration: parseFloat(metadata.format.duration),
        width: videoStream.width,
        height: videoStream.height,
        fps: eval(videoStream.r_frame_rate),
        hasAudio: !!audioStream,
      });
    });
  });
}
```

### 1B: Detect Scene Changes

```javascript
async function detectScenes(videoPath, outputDir) {
  // FFmpeg scene detection using select filter
  const sceneThreshold = 0.4; // Sensitivity: 0.3-0.5 (lower = more sensitive)

  const command = `ffmpeg -i "${videoPath}" ` +
    `-vf "select='gt(scene,${sceneThreshold})',metadata=print:file=${outputDir}/scenes.txt" ` +
    `-vsync vfr "${outputDir}/scene_%04d.jpg"`;

  await exec(command);

  // Parse scene timestamps
  const scenesData = require('fs').readFileSync(`${outputDir}/scenes.txt`, 'utf8');
  const scenes = [];
  const regex = /pts_time:(\d+\.?\d*)/g;
  let match;

  while ((match = regex.exec(scenesData)) !== null) {
    scenes.push(parseFloat(match[1]));
  }

  return scenes;
}
```

### 1C: Analyze Audio Levels

```javascript
async function analyzeAudioLevels(videoPath) {
  // Extract audio waveform data
  const command = `ffmpeg -i "${videoPath}" -af "astats=metadata=1:reset=1" -f null -`;

  const { stdout } = await exec(command);

  // Parse audio peaks to find high-energy moments
  const audioLevels = [];
  const lines = stdout.split('\n');

  for (const line of lines) {
    if (line.includes('Peak level')) {
      const match = line.match(/Peak level dB: ([-\d.]+)/);
      if (match) {
        audioLevels.push(parseFloat(match[1]));
      }
    }
  }

  return audioLevels;
}
```

---

## Step 2: Speech-to-Text Transcription

Use AssemblyAI to transcribe audio and detect key moments.

### 2A: Extract Audio Track

```javascript
async function extractAudio(videoPath, outputPath) {
  return new Promise((resolve, reject) => {
    ffmpeg(videoPath)
      .output(outputPath)
      .audioCodec('libmp3lame')
      .audioBitrate('128k')
      .noVideo()
      .on('end', resolve)
      .on('error', reject)
      .run();
  });
}
```

### 2B: Transcribe with AssemblyAI

```javascript
const { AssemblyAI } = require('assemblyai');

async function transcribeVideo(audioPath, apiKey) {
  const client = new AssemblyAI({ apiKey });

  // Upload audio file
  const transcript = await client.transcripts.transcribe({
    audio: audioPath,
    speaker_labels: true,           // Detect different speakers
    sentiment_analysis: true,       // Analyze sentiment
    auto_highlights: true,          // Auto-detect important moments
    content_safety: true,           // Filter inappropriate content
    iab_categories: true,           // Categorize content topics
  });

  if (transcript.status === 'error') {
    throw new Error(`Transcription failed: ${transcript.error}`);
  }

  return transcript;
}
```

### 2C: Extract Key Moments from Transcript

```javascript
function extractKeyMoments(transcript) {
  const keyMoments = [];

  // Extract auto-highlights (AssemblyAI's AI-detected important moments)
  if (transcript.auto_highlights_result?.results) {
    for (const highlight of transcript.auto_highlights_result.results) {
      keyMoments.push({
        type: 'highlight',
        text: highlight.text,
        start: highlight.timestamps[0].start / 1000,
        end: highlight.timestamps[highlight.timestamps.length - 1].end / 1000,
        confidence: highlight.rank,
      });
    }
  }

  // Extract high-sentiment moments (positive or negative extremes)
  if (transcript.sentiment_analysis_results) {
    for (const sentence of transcript.sentiment_analysis_results) {
      const sentimentScore = Math.abs(sentence.sentiment === 'POSITIVE' ? 1 :
                                      sentence.sentiment === 'NEGATIVE' ? -1 : 0);

      if (sentimentScore > 0 && sentence.confidence > 0.7) {
        keyMoments.push({
          type: 'sentiment',
          text: sentence.text,
          start: sentence.start / 1000,
          end: sentence.end / 1000,
          sentiment: sentence.sentiment,
          confidence: sentence.confidence,
        });
      }
    }
  }

  return keyMoments;
}
```

---

## Step 3: Segment Scoring Algorithm

Score each video segment based on multiple factors.

### 3A: Define Scoring Criteria

```javascript
const SCORING_WEIGHTS = {
  sceneChange: 0.15,        // Scene transitions indicate new content
  audioIntensity: 0.20,     // High audio = exciting moments
  speechHighlight: 0.30,    // AI-detected highlights
  sentiment: 0.15,          // Emotional peaks (positive or negative)
  speakerChange: 0.10,      // New speaker = potential key point
  contentSafety: 0.10,      // Ensure appropriate content
};

const SEGMENT_LENGTH = 10; // Analyze in 10-second segments
```

### 3B: Score Each Segment

```javascript
function scoreSegments(videoMetadata, scenes, audioLevels, transcript, keyMoments) {
  const segments = [];
  const duration = videoMetadata.duration;

  // Divide video into segments
  for (let start = 0; start < duration; start += SEGMENT_LENGTH) {
    const end = Math.min(start + SEGMENT_LENGTH, duration);

    const segment = {
      start,
      end,
      duration: end - start,
      scores: {},
      totalScore: 0,
    };

    // 1. Scene Change Score
    const sceneChanges = scenes.filter(s => s >= start && s < end).length;
    segment.scores.sceneChange = Math.min(sceneChanges / 3, 1) * SCORING_WEIGHTS.sceneChange;

    // 2. Audio Intensity Score
    const segmentAudio = audioLevels.slice(
      Math.floor(start),
      Math.ceil(end)
    );
    const avgAudioLevel = segmentAudio.reduce((a, b) => a + b, 0) / segmentAudio.length;
    const normalizedAudio = (avgAudioLevel + 60) / 60; // Normalize dB to 0-1
    segment.scores.audioIntensity = normalizedAudio * SCORING_WEIGHTS.audioIntensity;

    // 3. Speech Highlight Score
    const highlights = keyMoments.filter(
      m => m.type === 'highlight' && m.start >= start && m.start < end
    );
    const highlightScore = highlights.reduce((sum, h) => sum + h.confidence, 0) / highlights.length || 0;
    segment.scores.speechHighlight = highlightScore * SCORING_WEIGHTS.speechHighlight;

    // 4. Sentiment Score
    const sentiments = keyMoments.filter(
      m => m.type === 'sentiment' && m.start >= start && m.start < end
    );
    const sentimentScore = sentiments.reduce((sum, s) => sum + s.confidence, 0) / sentiments.length || 0;
    segment.scores.sentiment = sentimentScore * SCORING_WEIGHTS.sentiment;

    // 5. Speaker Change Score
    const speakers = transcript.utterances.filter(
      u => u.start / 1000 >= start && u.start / 1000 < end
    );
    const uniqueSpeakers = new Set(speakers.map(s => s.speaker)).size;
    segment.scores.speakerChange = Math.min(uniqueSpeakers / 2, 1) * SCORING_WEIGHTS.speakerChange;

    // 6. Content Safety Score (ensure appropriate content)
    const contentSafe = !transcript.content_safety?.summary?.some(
      item => item.timestamp >= start * 1000 && item.timestamp < end * 1000
    );
    segment.scores.contentSafety = contentSafe ? SCORING_WEIGHTS.contentSafety : 0;

    // Calculate total score
    segment.totalScore = Object.values(segment.scores).reduce((a, b) => a + b, 0);

    // Add transcript text for context
    segment.text = transcript.utterances
      .filter(u => u.start / 1000 >= start && u.start / 1000 < end)
      .map(u => u.text)
      .join(' ');

    segments.push(segment);
  }

  return segments.sort((a, b) => b.totalScore - a.totalScore);
}
```

### 3C: Select Top Clips

```javascript
function selectTopClips(rankedSegments, targetDuration = 60) {
  const selectedClips = [];
  let totalDuration = 0;

  // Avoid clips too close together (minimum 30s gap)
  const MIN_GAP = 30;

  for (const segment of rankedSegments) {
    // Check if this clip overlaps with already selected clips
    const tooClose = selectedClips.some(clip =>
      Math.abs(clip.start - segment.start) < MIN_GAP
    );

    if (!tooClose && totalDuration + segment.duration <= targetDuration) {
      selectedClips.push(segment);
      totalDuration += segment.duration;

      if (totalDuration >= targetDuration * 0.9) break; // 90% of target is sufficient
    }
  }

  // Sort clips chronologically for final video
  return selectedClips.sort((a, b) => a.start - b.start);
}
```

---

## Step 4: Extract Selected Clips

Use FFmpeg to extract the selected video segments.

```javascript
async function extractClips(videoPath, clips, outputDir) {
  const extractedClips = [];

  for (let i = 0; i < clips.length; i++) {
    const clip = clips[i];
    const outputPath = `${outputDir}/clip_${i + 1}.mp4`;

    // Extract clip with FFmpeg
    const command = `ffmpeg -ss ${clip.start} -i "${videoPath}" -t ${clip.duration} ` +
      `-c:v libx264 -c:a aac -strict experimental "${outputPath}"`;

    await exec(command);

    extractedClips.push({
      ...clip,
      path: outputPath,
      index: i,
    });

    console.log(`Extracted clip ${i + 1}/${clips.length}: ${clip.start}s - ${clip.end}s`);
  }

  return extractedClips;
}
```

---

## Step 5: Remotion Assembly & Rendering

Create Remotion composition to stitch clips with transitions.

### 5A: Remotion Template

```javascript
// HighlightReel.jsx
import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, Video, Audio, staticFile, Sequence } from 'remotion';

export const HighlightReel = ({ clips }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  let currentFrame = 0;

  return (
    <div style={{ width: '100%', height: '100%', backgroundColor: '#000' }}>
      {clips.map((clip, index) => {
        const clipDurationFrames = Math.floor(clip.duration * fps);
        const transitionFrames = 15; // 0.5s transition at 30fps

        const sequence = (
          <Sequence
            key={index}
            from={currentFrame}
            durationInFrames={clipDurationFrames + transitionFrames}
          >
            <ClipWithTransition
              clip={clip}
              index={index}
              transitionFrames={transitionFrames}
            />
          </Sequence>
        );

        currentFrame += clipDurationFrames;
        return sequence;
      })}

      {/* Background music (optional) */}
      <Audio src={staticFile('background-music.mp3')} volume={0.2} />
    </div>
  );
};

const ClipWithTransition = ({ clip, index, transitionFrames }) => {
  const frame = useCurrentFrame();

  // Fade in transition
  const fadeIn = interpolate(
    frame,
    [0, transitionFrames],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  // Zoom effect for dynamic feel
  const scale = interpolate(
    frame,
    [0, transitionFrames * 2],
    [1.05, 1],
    { extrapolateRight: 'clamp' }
  );

  return (
    <div style={{ opacity: fadeIn, transform: `scale(${scale})`, width: '100%', height: '100%' }}>
      <Video src={staticFile(`clip_${index + 1}.mp4`)} />

      {/* Clip number indicator */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          right: 40,
          fontSize: 32,
          color: 'white',
          fontWeight: 'bold',
          backgroundColor: 'rgba(0,0,0,0.6)',
          padding: '10px 20px',
          borderRadius: 8,
        }}
      >
        {index + 1}
      </div>
    </div>
  );
};
```

### 5B: Render Final Video

```javascript
// render-highlights.js
const { bundle } = require('@remotion/bundler');
const { renderMedia, selectComposition } = require('@remotion/renderer');
const path = require('path');

async function renderHighlightReel(clips, outputPath) {
  const compositionId = 'HighlightReel';

  // Bundle Remotion project
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./src/index.js'),
    webpackOverride: (config) => config,
  });

  // Get composition
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId,
    inputProps: { clips },
  });

  // Render video
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: outputPath,
    inputProps: { clips },
  });

  console.log(`✅ Highlight reel rendered: ${outputPath}`);
}
```

---

## Step 6: Main Orchestration Script

Tie all steps together in a single workflow.

```javascript
// create-highlights.js
const path = require('path');
const fs = require('fs').promises;

async function createVideoHighlights(videoPath, options = {}) {
  const {
    targetDuration = 60,        // Target length of highlight reel
    assemblyAIKey = process.env.ASSEMBLYAI_API_KEY,
    outputDir = './output',
  } = options;

  console.log('🎬 Starting Video Highlight Creator...\n');

  // Create output directory
  await fs.mkdir(outputDir, { recursive: true });

  try {
    // STEP 1: Analyze video metadata
    console.log('📊 Step 1: Analyzing video metadata...');
    const metadata = await getVideoMetadata(videoPath);
    console.log(`Duration: ${metadata.duration}s, Resolution: ${metadata.width}x${metadata.height}\n`);

    // STEP 2: Detect scenes
    console.log('🎥 Step 2: Detecting scene changes...');
    const scenes = await detectScenes(videoPath, outputDir);
    console.log(`Found ${scenes.length} scene changes\n`);

    // STEP 3: Analyze audio
    console.log('🔊 Step 3: Analyzing audio levels...');
    const audioLevels = await analyzeAudioLevels(videoPath);
    console.log(`Analyzed ${audioLevels.length} audio samples\n`);

    // STEP 4: Extract and transcribe audio
    console.log('🎙️ Step 4: Transcribing speech...');
    const audioPath = path.join(outputDir, 'audio.mp3');
    await extractAudio(videoPath, audioPath);
    const transcript = await transcribeVideo(audioPath, assemblyAIKey);
    console.log(`Transcription complete: ${transcript.words.length} words\n`);

    // STEP 5: Extract key moments
    console.log('✨ Step 5: Extracting key moments...');
    const keyMoments = extractKeyMoments(transcript);
    console.log(`Found ${keyMoments.length} key moments\n`);

    // STEP 6: Score segments
    console.log('📈 Step 6: Scoring video segments...');
    const rankedSegments = scoreSegments(metadata, scenes, audioLevels, transcript, keyMoments);
    console.log(`Scored ${rankedSegments.length} segments\n`);

    // STEP 7: Select top clips
    console.log('🎯 Step 7: Selecting top clips...');
    const selectedClips = selectTopClips(rankedSegments, targetDuration);
    console.log(`Selected ${selectedClips.length} clips (${selectedClips.reduce((sum, c) => sum + c.duration, 0)}s total)\n`);

    // STEP 8: Extract clips
    console.log('✂️ Step 8: Extracting video clips...');
    const extractedClips = await extractClips(videoPath, selectedClips, outputDir);
    console.log('Clips extracted successfully\n');

    // STEP 9: Render final highlight reel
    console.log('🎬 Step 9: Rendering final highlight reel...');
    const outputPath = path.join(outputDir, 'highlight-reel.mp4');
    await renderHighlightReel(extractedClips, outputPath);

    console.log('\n✅ Video highlights created successfully!');
    console.log(`📁 Output: ${outputPath}`);

    // Return analysis summary
    return {
      input: {
        duration: metadata.duration,
        resolution: `${metadata.width}x${metadata.height}`,
      },
      analysis: {
        scenes: scenes.length,
        keyMoments: keyMoments.length,
        totalSegments: rankedSegments.length,
      },
      output: {
        clips: selectedClips.length,
        totalDuration: selectedClips.reduce((sum, c) => sum + c.duration, 0),
        path: outputPath,
      },
    };

  } catch (error) {
    console.error('❌ Error creating highlights:', error);
    throw error;
  }
}

// CLI usage
if (require.main === module) {
  const videoPath = process.argv[2];

  if (!videoPath) {
    console.error('Usage: node create-highlights.js <video-path>');
    process.exit(1);
  }

  createVideoHighlights(videoPath)
    .then(summary => {
      console.log('\n📊 Summary:', JSON.stringify(summary, null, 2));
    })
    .catch(err => {
      console.error('Failed:', err.message);
      process.exit(1);
    });
}

module.exports = { createVideoHighlights };
```

---

## Usage Examples

### Example 1: Process a Webinar Recording

```bash
# Basic usage
node create-highlights.js "./recordings/webinar-2026-01-28.mp4"

# Custom duration (90 seconds)
node create-highlights.js "./recordings/webinar.mp4" --duration 90

# Specify output directory
node create-highlights.js "./recordings/webinar.mp4" --output "./highlights"
```

### Example 2: Programmatic Usage

```javascript
const { createVideoHighlights } = require('./create-highlights');

async function processVideo() {
  const result = await createVideoHighlights(
    './recordings/podcast-episode-42.mp4',
    {
      targetDuration: 75,
      outputDir: './podcast-highlights',
    }
  );

  console.log('Created highlight reel:', result.output.path);
  console.log('Clips used:', result.output.clips);
}

processVideo();
```

### Example 3: Batch Processing

```javascript
const videos = [
  './recordings/meeting-jan-20.mp4',
  './recordings/meeting-jan-21.mp4',
  './recordings/meeting-jan-22.mp4',
];

for (const video of videos) {
  await createVideoHighlights(video, {
    targetDuration: 60,
    outputDir: `./highlights/${path.basename(video, '.mp4')}`,
  });
}
```

---

## Configuration Options

### Scoring Weights Customization

Adjust scoring weights based on content type:

```javascript
// For technical presentations (focus on visuals)
const TECH_WEIGHTS = {
  sceneChange: 0.25,      // High - slide changes matter
  audioIntensity: 0.10,   // Low - often monotone
  speechHighlight: 0.35,  // High - key technical terms
  sentiment: 0.05,        // Low - neutral delivery
  speakerChange: 0.15,    // Medium - Q&A sections
  contentSafety: 0.10,
};

// For comedy/entertainment (focus on reactions)
const COMEDY_WEIGHTS = {
  sceneChange: 0.10,
  audioIntensity: 0.30,   // High - laughter, applause
  speechHighlight: 0.20,
  sentiment: 0.30,        // High - emotional peaks
  speakerChange: 0.05,
  contentSafety: 0.05,
};

// For interviews (focus on dialogue)
const INTERVIEW_WEIGHTS = {
  sceneChange: 0.05,
  audioIntensity: 0.15,
  speechHighlight: 0.35,
  sentiment: 0.20,
  speakerChange: 0.20,    // High - back and forth
  contentSafety: 0.05,
};
```

### AssemblyAI Advanced Options

```javascript
const transcript = await client.transcripts.transcribe({
  audio: audioPath,

  // Language detection
  language_detection: true,

  // Custom vocabulary (brand names, technical terms)
  word_boost: ['AI', 'machine learning', 'Nexius Labs'],
  boost_param: 'high',

  // Chapter detection for long videos
  auto_chapters: true,

  // Entity detection (people, organizations, locations)
  entity_detection: true,

  // Profanity filtering
  filter_profanity: true,

  // Dual channel (separate left/right audio)
  dual_channel: false,
});
```

---

## Output Structure

```
output/
├── audio.mp3                    # Extracted audio track
├── scenes.txt                   # Scene change timestamps
├── scene_0001.jpg              # Scene thumbnails
├── scene_0002.jpg
├── ...
├── transcript.json             # Full transcription data
├── segments-analysis.json      # Scored segments
├── clip_1.mp4                  # Individual clips
├── clip_2.mp4
├── clip_3.mp4
└── highlight-reel.mp4          # Final compiled video
```

---

## Performance Optimization

### Processing Time Estimates

| Video Length | Processing Time | Bottleneck |
|--------------|----------------|------------|
| 30 min | 5-8 minutes | Transcription (3-5 min) |
| 60 min | 10-15 minutes | Transcription (6-10 min) |
| 120 min | 20-30 minutes | Transcription (12-20 min) |

### Speed Improvements

```javascript
// 1. Parallel Processing
const [scenes, audioLevels, transcript] = await Promise.all([
  detectScenes(videoPath, outputDir),
  analyzeAudioLevels(videoPath),
  transcribeVideo(audioPath, apiKey),
]);

// 2. Lower Resolution Analysis (faster scene detection)
const command = `ffmpeg -i "${videoPath}" -vf "scale=640:-1,select='gt(scene,0.4)'" ...`;

// 3. Cache Transcriptions
const cacheKey = crypto.createHash('md5').update(audioPath).digest('hex');
const cachedTranscript = await redis.get(`transcript:${cacheKey}`);

// 4. Use AssemblyAI's faster model
const transcript = await client.transcripts.transcribe({
  audio: audioPath,
  speech_model: 'nano',  // Faster, slightly less accurate
});
```

---

## Quality Checklist

Before final render:
- [ ] All selected clips are content-safe (no inappropriate content)
- [ ] Clips are chronologically distributed (avoid clustering)
- [ ] Total duration matches target (±10%)
- [ ] Minimum 30-second gap between clips
- [ ] Audio levels normalized across clips
- [ ] Transitions are smooth (0.5s fade)
- [ ] No clips shorter than 5 seconds
- [ ] Representative coverage of full video (not all from first half)

---

## Troubleshooting

### Common Issues

**1. AssemblyAI Quota Exceeded**
```javascript
// Error: Free tier limit reached
// Solution: Upgrade to paid plan or wait for quota reset
// Alternative: Use local Whisper model (slower but free)
```

**2. FFmpeg Scene Detection Too Sensitive**
```javascript
// Too many scenes detected
// Solution: Increase threshold from 0.4 to 0.5-0.6
const sceneThreshold = 0.5; // Less sensitive
```

**3. No High-Scoring Segments**
```javascript
// All segments score low
// Solution: Adjust scoring weights or lower selection threshold
const selectedClips = selectTopClips(rankedSegments, targetDuration, { minScore: 0.3 });
```

**4. Remotion Render Fails**
```javascript
// Memory issues with long clips
// Solution: Reduce video quality or split rendering
await renderMedia({
  composition,
  quality: 70,  // Reduce from default 100
  scale: 0.8,   // Render at 80% size
});
```

---

## Edge Cases

### Very Long Videos (2+ hours)

```javascript
// Process in chunks to avoid memory issues
async function processLongVideo(videoPath, chunkSize = 1800) { // 30-min chunks
  const metadata = await getVideoMetadata(videoPath);
  const chunks = Math.ceil(metadata.duration / chunkSize);

  const allSegments = [];

  for (let i = 0; i < chunks; i++) {
    const start = i * chunkSize;
    const duration = Math.min(chunkSize, metadata.duration - start);

    const chunkPath = `./temp/chunk_${i}.mp4`;
    await extractVideoChunk(videoPath, start, duration, chunkPath);

    const chunkSegments = await analyzeVideoChunk(chunkPath);
    allSegments.push(...chunkSegments);
  }

  return allSegments;
}
```

### No Speech (Music Videos, B-Roll)

```javascript
// Fallback to visual analysis only
if (!metadata.hasAudio || transcript.words.length < 50) {
  console.warn('⚠️ Limited speech detected, using visual analysis only');

  const VISUAL_ONLY_WEIGHTS = {
    sceneChange: 0.40,
    audioIntensity: 0.30,
    motion: 0.30,  // Add motion detection
  };
}
```

### Multiple Languages

```javascript
// Auto-detect and handle multiple languages
const transcript = await client.transcripts.transcribe({
  audio: audioPath,
  language_detection: true,
});

console.log(`Detected language: ${transcript.language_code}`);
```

---

## Future Enhancements

### Planned Features

1. **Face Detection** - Prioritize segments with faces
2. **Motion Analysis** - Score based on video motion intensity
3. **Keyword Targeting** - Boost segments containing specific keywords
4. **Thumbnail Generation** - Auto-generate thumbnails for each clip
5. **Multi-Format Export** - Instagram Reels, YouTube Shorts, TikTok
6. **Custom Branding** - Add intro/outro, watermarks, lower thirds
7. **Interactive Preview** - Web UI to review and adjust clip selection
8. **ML-Based Scoring** - Train custom model on your video preferences

---

## Integration with Other Skills

| After This Skill | Use |
|------------------|-----|
| Created highlight reel | `instagram-reel-creator` - Add text overlays, music |
| Need thumbnail | `linkedin-image-generator` - Create cover image |
| Want to post | `instagram-reel-creator` - Upload to Instagram |

---

## Cost Analysis

### API Costs (AssemblyAI)

| Video Length | Transcription Cost | Free Tier Coverage |
|--------------|-------------------|-------------------|
| 30 min | $0.38 | 6 videos/month |
| 60 min | $0.75 | 3 videos/month |
| 120 min | $1.50 | 1-2 videos/month |

**Pricing:** $0.75 per audio hour
**Free Tier:** 3 hours per month

### Compute Costs

- FFmpeg: Free, local processing
- Remotion: Free, local rendering
- Storage: ~2GB per 60-min video processing

---

## Logging

Track processing details for debugging:

```javascript
// logs/highlight-creation.md
## Highlight Creation - [Date]

**Input Video:** path/to/video.mp4
Duration: 3600s (60 min)
Resolution: 1920x1080

**Analysis Results:**
- Scene changes: 247
- Key moments detected: 18
- Total segments scored: 360

**Selected Clips:**
1. 00:05:23 - 00:05:33 (10s) - Score: 0.87
2. 00:12:45 - 00:12:58 (13s) - Score: 0.82
3. 00:28:10 - 00:28:22 (12s) - Score: 0.79
...

**Output:**
Clips: 5
Total duration: 58s
Render time: 2m 34s
File size: 15.2 MB
```

---

## License & Attribution

- **FFmpeg**: LGPL/GPL (https://ffmpeg.org/legal.html)
- **AssemblyAI**: Commercial API (https://www.assemblyai.com/pricing)
- **Remotion**: Use requires license for commercial projects (https://remotion.dev/license)
- **Unsplash/Pixabay**: Royalty-free media sources

---

## Support & Resources

- **FFmpeg Docs**: https://ffmpeg.org/documentation.html
- **AssemblyAI Docs**: https://www.assemblyai.com/docs
- **Remotion Docs**: https://remotion.dev/docs
- **GitHub Issues**: Report bugs and feature requests

---

Created: 2026-01-28
Last Updated: 2026-01-28
Version: 1.0.0
