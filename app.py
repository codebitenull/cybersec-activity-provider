from factories.activity_factory import ActivityInstanceFactory
from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime
import uuid
import os
from adapters import SlideProvider, MockSlideAdapter, GoogleSlidesAdapter
from processors import BasicTrainingProcessor,AdvancedTrainingProcessor,CertificationTrainingProcessor

app = Flask(__name__)

# Mock data storage (em memória por agora)
activities = {}
instances = {}
analytics_data = {}

# ===== NOVO - TEMPLATE PATTERN (TÓPICO 6) =====
def get_processor(training_type, instance_data, student_id, slide_adapter):
    processors = {
        'basic': BasicTrainingProcessor,
        'advanced': AdvancedTrainingProcessor,
        'certification': CertificationTrainingProcessor
    }
    processor_class = processors.get(training_type, BasicTrainingProcessor)
    return processor_class(instance_data, student_id, slide_adapter)

# ===== NOVO - ADAPTER PATTERN (TÓPICO 5) =====

def get_slide_adapter(config):
    """
    Factory Method para criar adapter apropriado baseado na configuração.
    
    Combina Factory Method (Tópico 4) com Adapter (Tópico 5).
    
    Args:
        config: Configuração da atividade
    
    Returns:
        SlideProvider: Adapter apropriado
    """
    slide_source = config.get('slide_source', 'mock')
    slide_url = config.get('slide_url', '')
    
    if slide_source == 'google_slides':
        # Extrair presentation_id da URL
        if 'presentation/d/' in slide_url:
            presentation_id = slide_url.split('presentation/d/')[1].split('/')[0]
            return GoogleSlidesAdapter(presentation_id)
        else:
            print(f"Warning: Invalid Google Slides URL, using mock")
            return MockSlideAdapter()
    
    elif slide_source == 'powerpoint':
        # TODO: Implementar PowerPointAdapter no futuro
        print(f"Warning: PowerPoint not implemented, using mock")
        return MockSlideAdapter()
    
    else:
        # Default: mock adapter
        num_slides = config.get('num_slides', 10)
        return MockSlideAdapter(num_slides=num_slides)

# ===== FIM DO ADAPTER PATTERN =====



# ============================================
# ENDPOINT 1: GET /config
# ============================================
@app.route('/config', methods=['GET'])
def get_config():
    """Retorna página HTML de configuração"""
    return render_template('config.html')

# ============================================
# ENDPOINT 2: GET /json-params
# ============================================
@app.route('/json-params', methods=['GET'])
def get_json_params():
    """Retorna schema de parâmetros configuráveis"""
    params = [
        {"name": "tituloFormacao", "type": "text/plain"},
        {"name": "descricao", "type": "text/plain"},
        {"name": "urlApresentacao", "type": "text/plain"},
        {"name": "numQuestoesPorQuiz", "type": "integer"},
        {"name": "notaMinimaAprovacao", "type": "integer"},
        {"name": "tempoLimiteMinutos", "type": "integer"}
    ]
    return jsonify(params)

# ============================================
# ENDPOINT 3: POST /deploy
# ============================================
@app.route('/deploy', methods=['POST'])
def deploy():
    """Cria instância de atividade para estudante - USANDO FACTORY METHOD"""
    try:
        data = request.json
        
        # Extrair dados do pedido Inven!RA
        activity_id = data.get('activityID')
        student_id = data.get('inveniraStdID')
        json_params = data.get('json_params', {})
        
        # USAR FACTORY METHOD para criar instância apropriada
        factory = ActivityInstanceFactory()
        instance = factory.create_instance(activity_id, student_id, json_params)
        
        # Armazenar instância (converter para dict)
        instances[instance.instance_id] = instance.to_dict()
        
        # Gerar URL de acesso
        base_url = request.url_root.rstrip('/')
        access_url = f"{base_url}/training/{instance.instance_id}"
        
        return jsonify({
            "url": access_url,
            "instanceType": instance.get_training_type(),
            "durationMinutes": instance.get_duration_minutes(),
            "requiresCertification": instance.requires_certification()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# ENDPOINT 4: GET /analytics-list
# ============================================
@app.route('/analytics-list', methods=['GET'])
def get_analytics_list():
    """Retorna schema de analytics disponíveis"""
    schema = {
        "qualAnalytics": [
            {"name": "ComentariosFinais", "type": "text/plain"},
            {"name": "URLCertificado", "type": "URL"}
        ],
        "quantAnalytics": [
            {"name": "AcessouFormacao", "type": "boolean"},
            {"name": "SlidesVisualizados", "type": "integer"},
            {"name": "TotalSlides", "type": "integer"},
            {"name": "PercentagemConclusao", "type": "integer"},
            {"name": "Quiz1Nota", "type": "integer"},
            {"name": "Quiz1Passou", "type": "boolean"},
            {"name": "Quiz2Nota", "type": "integer"},
            {"name": "Quiz2Passou", "type": "boolean"},
            {"name": "TempoTotalMinutos", "type": "integer"},
            {"name": "ConcluiuFormacao", "type": "boolean"}
        ]
    }
    return jsonify(schema)

# ============================================
# ENDPOINT 5: POST /analytics
# ============================================
@app.route('/analytics', methods=['POST'])
def get_analytics():
    """Retorna analytics de uma atividade"""
    try:
        data = request.json
        activity_id = data.get('activityID')
        
        # Mock data - retornar dados de exemplo
        mock_analytics = [
            {
                "inveniraStdID": "student123",
                "quantAnalytics": [
                    {"name": "AcessouFormacao", "type": "boolean", "value": True},
                    {"name": "SlidesVisualizados", "type": "integer", "value": 45},
                    {"name": "TotalSlides", "type": "integer", "value": 50},
                    {"name": "PercentagemConclusao", "type": "integer", "value": 90},
                    {"name": "Quiz1Nota", "type": "integer", "value": 85},
                    {"name": "Quiz1Passou", "type": "boolean", "value": True},
                    {"name": "Quiz2Nota", "type": "integer", "value": 92},
                    {"name": "Quiz2Passou", "type": "boolean", "value": True},
                    {"name": "TempoTotalMinutos", "type": "integer", "value": 75},
                    {"name": "ConcluiuFormacao", "type": "boolean", "value": True}
                ],
                "qualAnalytics": [
                    {"name": "ComentariosFinais", "type": "text/plain", 
                     "value": "Formação muito útil para o dia-a-dia hospitalar"},
                    {"name": "URLCertificado", "type": "URL", 
                     "value": f"{request.url_root}cert/abc123"}
                ]
            }
        ]
        
        return jsonify(mock_analytics)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ============================================
# ROTA ADICIONAL: Página da formação
# ============================================
@app.route('/training/<instance_id>')
def training(instance_id):
    """
    Endpoint de formação usando Adapter Pattern (Tópico 5).
    
    Demonstra uso do SlideProvider sem conhecer fonte real.
    """
    # Verificar se instância existe
    if instance_id not in instances:
        return jsonify({"error": "Training instance not found"}), 404
    
    instance_data = instances[instance_id]
    config = instance_data.get('config', {})
    
    # ADAPTER PATTERN: Obter adapter apropriado
    slide_adapter = get_slide_adapter(config)
    
    # Activity Manager trabalha com interface comum
    try:
        total_slides = slide_adapter.get_total_slides()
        all_slides = slide_adapter.get_all_slides()
        
        return jsonify({
            'instance_id': instance_id,
            'title': config.get('title', 'Training'),
            'type': instance_data.get('type', 'basic'),
            'duration_minutes': instance_data.get('durationMinutes', 30),
            'total_slides': total_slides,
            'slides': all_slides,
            'current_slide': 1
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ============================================
#  
# ============================================

@app.route('/training/<instance_id>/slide/<int:slide_num>')
def get_slide(instance_id, slide_num):
    """
    Endpoint para obter slide específico (Adapter Pattern).
    """
    if instance_id not in instances:
        return jsonify({"error": "Training instance not found"}), 404
    
    instance_data = instances[instance_id]
    config = instance_data.get('config', {})
    
    # ADAPTER PATTERN
    slide_adapter = get_slide_adapter(config)
    
    try:
        slide_content = slide_adapter.get_slide_content(slide_num)
        thumbnail = slide_adapter.get_slide_thumbnail(slide_num)
        
        return jsonify({
            'instance_id': instance_id,
            'slide': slide_content,
            'thumbnail': thumbnail,
            'navigation': {
                'current': slide_num,
                'total': slide_adapter.get_total_slides(),
                'has_previous': slide_num > 1,
                'has_next': slide_num < slide_adapter.get_total_slides()
            }
        })
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500






# ============================================
# HEALTH CHECK
# ============================================
@app.route('/health', methods=['GET'])
def health():
    """Verificar se servidor está up"""
    return jsonify({
        "status": "ok", 
        "timestamp": datetime.now().isoformat(),
        "service": "Cybersecurity Training Activity Provider",
        "version": "1.0.0"
    })

# ============================================
# ROOT - Página de boas-vindas
# ============================================
@app.route('/', methods=['GET'])
def index():
    """Página inicial"""
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Activity Provider - Cibersegurança</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px 20px;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            h1 { font-size: 3em; margin-bottom: 10px; }
            h2 { font-size: 1.5em; font-weight: 300; margin-bottom: 30px; }
            .endpoints {
                text-align: left;
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
            }
            .endpoint {
                margin: 10px 0;
                font-family: 'Courier New', monospace;
            }
            .badge {
                display: inline-block;
                padding: 3px 10px;
                background: #27ae60;
                border-radius: 5px;
                font-size: 0.8em;
                margin-right: 10px;
            }
            a { color: #ffd700; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Activity Provider</h1>
            <h2>Formação em Cibersegurança Hospitalar</h2>
            
            <p>Serviço RESTful para integração com plataforma Inven!RA</p>
            
            <div class="endpoints">
                <h3>📡 Endpoints Disponíveis:</h3>
                <div class="endpoint">
                    <span class="badge">GET</span>
                    <a href="/config">/config</a> - Página de configuração
                </div>
                <div class="endpoint">
                    <span class="badge">GET</span>
                    <a href="/json-params">/json-params</a> - Schema de parâmetros
                </div>
                <div class="endpoint">
                    <span class="badge">POST</span>
                    /deploy - Criar instância de formação
                </div>
                <div class="endpoint">
                    <span class="badge">GET</span>
                    <a href="/analytics-list">/analytics-list</a> - Schema de analytics
                </div>
                <div class="endpoint">
                    <span class="badge">POST</span>
                    /analytics - Obter analytics de atividade
                </div>
                <div class="endpoint">
                    <span class="badge">GET</span>
                    <a href="/health">/health</a> - Health check
                </div>
            </div>
            
            <p style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
                Desenvolvido por Artur Miranda | Mestrado Eng. Informática | 2025
            </p>
        </div>
    </body>
    </html>
    """


# ============================================
# 
# ============================================
@app.route('/training/<instance_id>/process', methods=['POST'])
def process_training(instance_id):
    """Processa formação usando Template Method Pattern"""
    if instance_id not in instances:
        return jsonify({"error": "Training instance not found"}), 404
    
    data = request.get_json()
    student_id = data.get('student_id')
    
    if not student_id:
        return jsonify({"error": "student_id required"}), 400
    
    instance_data = instances[instance_id]
    config = instance_data.get('config', {})
    training_type = instance_data.get('type', 'basic')
    
    # Adapter Pattern (Tópico 5)
    slide_adapter = get_slide_adapter(config)
    
    # Template Method Pattern (Tópico 6)
    processor = get_processor(training_type, instance_data, student_id, slide_adapter)
    
    try:
        result = processor.process()
        return jsonify({'instance_id': instance_id, 'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
#  Processa formação
# ============================================
@app.route('/training/<instance_id>/workflow', methods=['GET'])
def get_workflow_info(instance_id):
    """Mostra workflow do Template Method"""
    if instance_id not in instances:
        return jsonify({"error": "Training instance not found"}), 404
    
    instance_data = instances[instance_id]
    training_type = instance_data.get('type', 'basic')
    
    workflows = {
        'basic': {
            'steps': ['1. Validate (no requirements)', '2. Load slides', 
                     '3. Initialize', '4. Evaluate (>=70%)', '5. Finalize'],
            'passing_score': 70,
            'certification': False
        },
        'advanced': {
            'steps': ['1. Validate (basic required)', '2. Load slides',
                     '3. Initialize', '4. Evaluate (>=80%)', '5. Finalize + RGPD cert'],
            'passing_score': 80,
            'certification': 'RGPD'
        },
        'certification': {
            'steps': ['1. Validate (advanced + exp)', '2. Load slides',
                     '3. Initialize', '4. Evaluate weighted (>=85%)', '5. Finalize + pro cert'],
            'passing_score': 85,
            'certification': 'Professional'
        }
    }
    
    return jsonify({
        'instance_id': instance_id,
        'workflow': workflows.get(training_type, workflows['basic']),
        'pattern': 'Template Method'
    })


# ============================================
# MAIN - Compatível com Render/Gunicorn
# ============================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)