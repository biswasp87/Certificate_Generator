import os
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from models import db, Template, ExcelColumn, ExcelRow
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certificate_generator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

# Ensure upload directories exist
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'templates'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'signatures'), exist_ok=True)
os.makedirs('fonts/Hindi Font', exist_ok=True)
os.makedirs('fonts/English Font', exist_ok=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    print("Received upload_excel request")
    if 'file' not in request.files:
        print("Error: No file part in request")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        print("Error: No selected file")
        return jsonify({'error': 'No selected file'}), 400

    print(f"Reading excel file: {file.filename}")
    try:
        df = pd.read_excel(file)
        print(f"Excel file read successfully. Columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error reading excel file: {str(e)}")
        return jsonify({'error': f'Failed to read Excel file: {str(e)}'}), 500

    columns = df.columns.tolist()
    # Temporarily store data in session or a temporary file?
    # For simplicity, let's just return the columns and the data to the frontend to send back.
    # Or save to a global variable (not recommended but okay for this task).
    # Better: save as a temporary JSON or in DB.

    # Let's save the data rows to ExcelRow temporarily or just return them.
    data = df.to_dict(orient='records')

    return jsonify({'columns': columns, 'data': data})

@app.route('/save_mapping', methods=['POST'])
def save_mapping():
    print("Received save_mapping request")
    req_data = request.json
    columns_info = req_data.get('columns', []) # list of {name, is_hindi}
    rows_data = req_data.get('data', [])

    # Clear old data
    db.session.query(ExcelColumn).delete()
    db.session.query(ExcelRow).delete()

    for col in columns_info:
        new_col = ExcelColumn(name=col['name'], is_hindi=col['is_hindi'])
        db.session.add(new_col)

    for row in rows_data:
        new_row = ExcelRow(data=row)
        db.session.add(new_row)

    db.session.commit()
    return jsonify({'message': 'Data saved successfully'})

@app.route('/fonts', methods=['GET'])
def get_fonts():
    hindi_fonts = os.listdir('fonts/Hindi Font')
    english_fonts = os.listdir('fonts/English Font')
    return jsonify({
        'hindi': [f for f in hindi_fonts if f.endswith(('.ttf', '.otf'))],
        'english': [f for f in english_fonts if f.endswith(('.ttf', '.otf'))]
    })

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/font_files/<path:path>')
def get_font_file(path):
    return send_from_directory('fonts', path)

@app.route('/templates', methods=['GET'])
def list_templates():
    templates = Template.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'image_path': t.image_path,
        'width': t.width,
        'height': t.height,
        'sig1_path': t.sig1_path,
        'sig2_path': t.sig2_path,
        'sig3_path': t.sig3_path,
        'sig4_path': t.sig4_path,
        'config': t.config
    } for t in templates])

@app.route('/upload_template', methods=['POST'])
def upload_template():
    print(f"Received upload_template request for: {request.form.get('name')}")
    name = request.form.get('name', 'Untitled')
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file'}), 400

    safe_name = secure_filename(name)
    safe_filename = secure_filename(file.filename)
    filename = f"template_{safe_name}_{safe_filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'templates', filename)
    file.save(filepath)

    with Image.open(filepath) as img:
        width, height = img.size

    new_template = Template(
        name=name,
        image_path=f"templates/{filename}",
        width=width,
        height=height
    )
    db.session.add(new_template)
    db.session.commit()
    return jsonify({'id': new_template.id, 'width': width, 'height': height})

@app.route('/update_template/<int:template_id>', methods=['POST'])
def update_template(template_id):
    template = Template.query.get_or_404(template_id)
    req_data = request.json
    template.config = req_data.get('config', template.config)
    db.session.commit()
    return jsonify({'message': 'Template updated'})

@app.route('/delete_template/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    template = Template.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({'message': 'Template deleted'})

@app.route('/upload_signatures/<int:template_id>', methods=['POST'])
def upload_signatures(template_id):
    template = Template.query.get_or_404(template_id)
    for i in range(1, 5):
        file = request.files.get(f'sig{i}')
        if file:
            safe_filename = secure_filename(file.filename)
            filename = f"sig{i}_{template.id}_{safe_filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'signatures', filename)
            file.save(filepath)
            setattr(template, f'sig{i}_path', f"signatures/{filename}")

    db.session.commit()
    return jsonify({'message': 'Signatures uploaded'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
