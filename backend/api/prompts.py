"""
Prompt templates per la generazione di contenuti
"""

def get_strategy_prompt(niche, target_audience, goals, posting_frequency):
    """Genera il prompt per la strategia di contenuto"""
    return f"""
You are an expert social media strategist. Create a comprehensive Instagram content strategy.

**Client Information:**
- Niche: {niche}
- Target Audience: {target_audience}
- Goals: {goals}
- Posting Frequency: {posting_frequency}

**IMPORTANT: Respond ONLY with valid JSON. Do not wrap it in markdown code blocks.**

Generate a strategy with this EXACT structure:

{{
  "content_pillars": [
    {{"name": "Pillar 1", "description": "Why it resonates"}},
    {{"name": "Pillar 2", "description": "Why it resonates"}},
    {{"name": "Pillar 3", "description": "Why it resonates"}}
  ],
  "calendar": [
    // Generate exactly 30 daily entries with this structure:
    {{"day": 1, "post_type": "Reel/Post/Carousel", "pillar": "Which pillar", "topic": "Post topic", "hook": "First line caption", "best_time": "HH:MM AM/PM"}}
  ],
  "hashtags": {{
    "niche": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
    "trending": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
    "engagement": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"]
  }},
  "posting_times": [
    {{"day": "Monday", "times": ["9:00 AM", "3:00 PM"]}},
    {{"day": "Tuesday", "times": ["9:00 AM", "3:00 PM"]}}
  ],
  "engagement_tips": [
    "Tip 1",
    "Tip 2",
    "Tip 3",
    "Tip 4",
    "Tip 5"
  ]
}}

**Requirements:**
- Calendar MUST have EXACTLY 30 entries (one for each day of the month)
- Each hashtag category MUST have EXACTLY 5 hashtags
- Distribute posts evenly across the 3 content pillars
- Make topics specific and actionable
- Hooks should be attention-grabbing first lines
- Best times should vary throughout the day

Return ONLY the JSON object, nothing else.
"""


def get_regenerate_strategy_prompt(previous_strategy, feedback):
    """Genera il prompt per rigenerare una strategia"""
    return f"""
You are an expert social media strategist. A client is not satisfied with their current strategy and provided feedback.

**Current Strategy:**
{previous_strategy}

**Client Feedback:**
{feedback}

**Task:**
Regenerate and improve the strategy addressing the client's concerns. Maintain the same structure but:
1. Address all points mentioned in the feedback
2. Provide fresh, innovative ideas
3. Keep what worked well
4. Enhance weak areas

Format your response in the same JSON structure as before:
- content_pillars
- calendar
- hashtags
- posting_times
- engagement_tips

Make sure the new strategy directly addresses the feedback while maintaining professional quality.
"""


def get_content_prompt(topic, post_type, tone, target_audience):
    """Genera il prompt per creare contenuto specifico"""
    return f"""
You are an expert Instagram content creator. Generate a complete post for Instagram.

**Content Brief:**
- Topic: {topic}
- Post Type: {post_type}
- Tone: {tone}
- Target Audience: {target_audience}

**Generate:**

1. **Caption** (engaging and optimized for Instagram)
   - Hook in the first line
   - Value-driven content
   - Clear call-to-action
   - Emojis where appropriate
   - 150-200 words

2. **Hashtags** (25-30 relevant hashtags)
   - Mix of popular and niche-specific
   - Categorized by size (high/medium/low volume)

3. **Visual Suggestions**
   - Description of what the image/video should show
   - Color scheme suggestions
   - Composition ideas

4. **Posting Recommendations**
   - Best time to post
   - Estimated engagement potential
   - Tips to boost performance

Format as JSON:
{{
  "caption": "...",
  "hashtags": ["...", "..."],
  "visual_suggestions": {{
    "description": "...",
    "colors": ["...", "..."],
    "composition": "..."
  }},
  "posting_recommendations": {{
    "best_time": "...",
    "engagement_tips": ["...", "..."]
  }}
}}
"""


def get_trending_reels_prompt(niche, target_audience):
    """Genera il prompt per idee di reels trending"""
    return f"""
You are a viral content strategist specializing in Instagram Reels.

**Client Info:**
- Niche: {niche}
- Target Audience: {target_audience}

**Task:** Generate 10 trending Reel ideas that have high viral potential for this niche.

For each idea, provide:

1. **Title** - Catchy, attention-grabbing title
2. **Hook** (First 3 seconds) - What captures attention immediately
3. **Content Structure** - Step-by-step breakdown
4. **Trending Audio Suggestion** - Type of music/sound that works
5. **Visual Style** - How it should look
6. **Call-to-Action** - What action to prompt
7. **Viral Potential Score** - Rate 1-10 with explanation
8. **Estimated Engagement** - Expected likes/comments/shares

**Current Trends to Consider:**
- Educational content in entertaining format
- Behind-the-scenes
- Transformation/before-after
- Trending challenges adapted to niche
- Storytelling with emotional hooks

Format as JSON array:
[
  {{
    "title": "...",
    "hook": "...",
    "structure": ["step1", "step2", "..."],
    "audio_suggestion": "...",
    "visual_style": "...",
    "call_to_action": "...",
    "viral_score": 8,
    "viral_explanation": "...",
    "estimated_engagement": "..."
  }},
  ...
]

Make ideas specific, actionable, and optimized for current Instagram algorithm.
"""


def get_optimize_idea_prompt(idea_content, optimization_goal):
    """Genera il prompt per ottimizzare un'idea"""
    return f"""
You are an expert content optimizer for Instagram.

**Original Idea:**
{idea_content}

**Optimization Goal:**
{optimization_goal}

**Task:** Improve and optimize this content idea to maximize {optimization_goal}.

Provide:

1. **Optimized Version** - Improved iteration of the idea
2. **Key Changes** - What was changed and why
3. **Enhancement Suggestions** - Additional ways to improve
4. **A/B Testing Ideas** - Variations to test
5. **Success Metrics** - What to measure

Format as JSON:
{{
  "optimized_content": {{
    "title": "...",
    "description": "...",
    "implementation": ["step1", "step2", "..."]
  }},
  "key_changes": ["change1", "change2", "..."],
  "enhancements": ["tip1", "tip2", "..."],
  "ab_test_variations": [
    {{"variation": "A", "description": "..."}},
    {{"variation": "B", "description": "..."}}
  ],
  "success_metrics": ["metric1", "metric2", "..."]
}}

Focus on practical, implementable improvements that align with Instagram's best practices.
"""