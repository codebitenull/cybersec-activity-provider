from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime
import uuid
import os

app = Flask(__name__)

# Mock data storage (em memória por agora)
activities = {}
instances = {}
analytics_data = {}

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
    """Cria instância de atividade para estudante"""
    try:
        data = request.json
        
        # Extrair dados do pedido Inven!RA
        activity_id = data.get('activityID')
        student_id = data.get('inveniraStdID')
        json_params = data.get('json_params', {})
        
        # Criar instância única
        instance_id = str(uuid.uuid4())
        
        # Armazenar instância (mock)
        instances[instance_id] = {
            'activityID': activity_id,
            'studentID': student_id,
            'config': json_params,
            'createdAt': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Gerar URL de acesso
        base_url = request.url_root.rstrip('/')
        access_url = f"{base_url}/training/{instance_id}"
        
        return jsonify({"url": access_url})
    
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
@app.route('/training/<instance_id>', methods=['GET'])
def training_page(instance_id):
    """Página onde estudante acede à formação"""
    if instance_id in instances:
        instance = instances[instance_id]
        return f"""
        <!DOCTYPE html>
        <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Formação em Cibersegurança</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 900px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f0f8ff;
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                .info {{
                    background: #ecf0f1;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .status {{
                    display: inline-block;
                    padding: 5px 15px;
                    background: #27ae60;
                    color: white;
                    border-radius: 20px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛡️ Formação em Cibersegurança Hospitalar</h1>
                
                <div class="info">
                    <p><strong>Instância ID:</strong> {instance_id}</p>
                    <p><strong>Estudante ID:</strong> {instance['studentID']}</p>
                    <p><strong>Status:</strong> <span class="status">{instance['status']}</span></p>
                    <p><strong>Criada em:</strong> {instance['createdAt']}</p>
                </div>
                
                <h2>📚 Conteúdo da Formação</h2>
                <p>Esta interface será desenvolvida nas próximas semanas com:</p>
                <ul>
                    <li>Visualizador de slides interativo</li>
                    <li>Quizzes de avaliação</li>
                    <li>Tracking de progressão</li>
                    <li>Certificado final</li>
                </ul>
                
                <p style="margin-top: 30px; color: #7f8c8d; font-size: 14px;">
                    <em>Protótipo - Semana 1 - Activity Provider</em>
                </p>
            </div>
        </body>
        </html>
        """
    else:
        return """
        <!DOCTYPE html>
        <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <title>Erro</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; }
                h1 { color: #e74c3c; }
            </style>
        </head>
        <body>
            <h1>⚠️ Instância não encontrada</h1>
            <p>A instância solicitada não existe ou expirou.</p>
        </body>
        </html>
        """, 404

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
# MAIN - Compatível com Render/Gunicorn
# ============================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)