"""
Prompt templates per la generazione di contenuti
"""

def get_strategy_prompt(niche, target_audience, goals, posting_frequency):
    """Genera il prompt per la strategia di contenuto"""
    return f"""
You are an expert social media strategist and content creator. Create a comprehensive content strategy for Instagram.

**Client Information:**
- Niche: {niche}
- Target Audience: {target_audience}
- Goals: {goals}
- Posting Frequency: {posting_frequency}

**Generate a detailed strategy including:**

1. **Content Pillars** (3-5 main themes)
   - List each pillar with a brief description
   - Explain why it resonates with the target audience

2. **Monthly Content Calendar** (30 days)
   - Create a day-by-day posting schedule
   - Include: Post Type (Reel/Post/Carousel), Topic, Hook/Caption idea, Best posting time
   - Distribute content across the pillars
   - Format as a structured table or list

3. **Hashtag Strategy**
   - 5 niche-specific hashtags
   - 5 trending/popular hashtags
   - 5 engagement-focused hashtags

4. **Optimal Posting Times**
   - Best times to post based on target audience
   - Include specific hours and days

5. **Engagement Strategy**
   - Tips for increasing engagement
   - Call-to-action suggestions
   - Community building tactics

Format your response in clear, structured JSON format with these keys:
- content_pillars: array of objects with 'name' and 'description'
- calendar: array of 30 objects with 'day', 'post_type', 'pillar', 'topic', 'hook', 'best_time'
- hashtags: object with 'niche', 'trending', 'engagement' arrays
- posting_times: array of objects with 'day' and 'times'
- engagement_tips: array of strings

Make it actionable, specific to the niche, and optimized for Instagram's algorithm.
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