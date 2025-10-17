import json
import re
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .prompts import (
    get_strategy_prompt,
    get_content_prompt,
    get_trending_reels_prompt,
    get_optimize_idea_prompt,
    get_regenerate_strategy_prompt
)


def clean_json_response(text):
    """Pulisce la risposta da markdown code blocks e altri artifacts"""
    if not text:
        return ""
    
    # Rimuovi markdown code blocks
    text = re.sub(r'^```json\s*', '', text.strip())
    text = re.sub(r'^```\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text.strip())
    
    # Rimuovi eventuali spazi extra
    text = text.strip()
    
    return text


def call_ollama(prompt, temperature=0.7, max_tokens=2000):
    """Helper function per chiamare Ollama"""
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                'model': settings.OLLAMA_MODEL,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': temperature,
                    'num_predict': max_tokens,
                    'num_ctx': 2048
                }
            },
            timeout=600
        )
        
        if response.status_code == 200:
            result = response.json()
            raw_response = result.get('response', '')
            
            # Pulisci la risposta
            cleaned_response = clean_json_response(raw_response)
            
            return cleaned_response
        else:
            raise Exception(f"Ollama returned status {response.status_code}: {response.text}")
    
    except Exception as e:
        raise Exception(f"Failed to connect to Ollama: {str(e)}")


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django backend is running',
        'ollama_url': settings.OLLAMA_BASE_URL,
        'ollama_model': settings.OLLAMA_MODEL
    })


@csrf_exempt
@require_http_methods(["POST", "GET"])
def test_ollama(request):
    """Test Ollama connection"""
    try:
        if request.method == "GET":
            prompt = "Say 'Hello, I am working!' in one sentence."
        else:
            data = json.loads(request.body)
            prompt = data.get('prompt', 'Hello, how are you?')
        
        response_text = call_ollama(prompt, max_tokens=500)
        
        return JsonResponse({
            'success': True,
            'response': response_text,
            'model': settings.OLLAMA_MODEL
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_strategy(request):
    """Genera una strategia di contenuto completa"""
    try:
        data = json.loads(request.body)
        
        niche = data.get('niche', '')
        target_audience = data.get('target_audience', 'General audience')
        goals = data.get('goals', 'Increase engagement')
        posting_frequency = data.get('posting_frequency', '3-5 posts per week')
        
        if not niche:
            return JsonResponse({
                'success': False,
                'error': 'Niche is required'
            }, status=400)
        
        prompt = get_strategy_prompt(niche, target_audience, goals, posting_frequency)
        response_text = call_ollama(prompt, temperature=0.8, max_tokens=4000)
        
        # Prova a parsare come JSON
        try:
            strategy_json = json.loads(response_text)
            
            return JsonResponse({
                'success': True,
                'strategy': strategy_json,
                'metadata': {
                    'niche': niche,
                    'target_audience': target_audience,
                    'goals': goals,
                    'posting_frequency': posting_frequency
                }
            })
        except json.JSONDecodeError as e:
            # Se il parsing fallisce, restituisci comunque il testo pulito
            return JsonResponse({
                'success': True,
                'strategy': response_text,
                'metadata': {
                    'niche': niche,
                    'target_audience': target_audience,
                    'goals': goals,
                    'posting_frequency': posting_frequency
                },
                'warning': f'Response was not valid JSON: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate strategy.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_content(request):
    """Genera contenuto per un singolo post"""
    try:
        data = json.loads(request.body)
        
        topic = data.get('topic', '')
        post_type = data.get('post_type', 'post')
        tone = data.get('tone', 'professional')
        target_audience = data.get('target_audience', 'General audience')
        
        if not topic:
            return JsonResponse({
                'success': False,
                'error': 'Topic is required'
            }, status=400)
        
        prompt = get_content_prompt(topic, post_type, tone, target_audience)
        response_text = call_ollama(prompt, temperature=0.7, max_tokens=1500)
        
        try:
            content_json = json.loads(response_text)
            
            return JsonResponse({
                'success': True,
                'content': content_json,
                'metadata': {
                    'topic': topic,
                    'post_type': post_type,
                    'tone': tone,
                    'target_audience': target_audience
                }
            })
        except json.JSONDecodeError as e:
            return JsonResponse({
                'success': True,
                'content': response_text,
                'metadata': {
                    'topic': topic,
                    'post_type': post_type,
                    'tone': tone,
                    'target_audience': target_audience
                },
                'warning': f'Response was not valid JSON: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate content.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_trending_reels(request):
    """Genera 10 idee per reels trending"""
    try:
        data = json.loads(request.body)
        
        niche = data.get('niche', 'content creation')
        target_audience = data.get('target_audience', 'General audience')
        
        prompt = get_trending_reels_prompt(niche, target_audience)
        response_text = call_ollama(prompt, temperature=0.9, max_tokens=3000)
        
        try:
            ideas_json = json.loads(response_text)
            
            return JsonResponse({
                'success': True,
                'ideas': ideas_json,
                'metadata': {
                    'niche': niche,
                    'target_audience': target_audience
                }
            })
        except json.JSONDecodeError as e:
            return JsonResponse({
                'success': True,
                'ideas': response_text,
                'metadata': {
                    'niche': niche,
                    'target_audience': target_audience
                },
                'warning': f'Response was not valid JSON: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate trending reels.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def optimize_idea(request):
    """Ottimizza un'idea di contenuto esistente"""
    try:
        data = json.loads(request.body)
        
        idea_content = data.get('idea_content', '')
        optimization_goal = data.get('optimization_goal', 'engagement')
        
        if not idea_content:
            return JsonResponse({
                'success': False,
                'error': 'Idea content is required'
            }, status=400)
        
        prompt = get_optimize_idea_prompt(idea_content, optimization_goal)
        response_text = call_ollama(prompt, temperature=0.7, max_tokens=1500)
        
        try:
            optimized_json = json.loads(response_text)
            
            return JsonResponse({
                'success': True,
                'optimized_idea': optimized_json,
                'original_idea': idea_content
            })
        except json.JSONDecodeError as e:
            return JsonResponse({
                'success': True,
                'optimized_idea': response_text,
                'original_idea': idea_content,
                'warning': f'Response was not valid JSON: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to optimize idea.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def regenerate_strategy(request):
    """Rigenera una strategia basata su feedback"""
    try:
        data = json.loads(request.body)
        
        previous_strategy = data.get('previous_strategy', '')
        feedback = data.get('feedback', '')
        
        if not feedback:
            return JsonResponse({
                'success': False,
                'error': 'Feedback is required'
            }, status=400)
        
        prompt = get_regenerate_strategy_prompt(previous_strategy, feedback)
        response_text = call_ollama(prompt, temperature=0.8, max_tokens=4000)
        
        try:
            strategy_json = json.loads(response_text)
            
            return JsonResponse({
                'success': True,
                'strategy': strategy_json,
                'feedback_applied': feedback
            })
        except json.JSONDecodeError as e:
            return JsonResponse({
                'success': True,
                'strategy': response_text,
                'feedback_applied': feedback,
                'warning': f'Response was not valid JSON: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to regenerate strategy.'
        }, status=500)