import os
import uuid
import logging
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import db
from models import GeneratedImage
from utils import generate_image_from_text, get_available_models

logger = logging.getLogger(__name__)

def register_routes(app):
    
    @app.route('/')
    def index():
        """Main page with text-to-image generation form"""
        models = get_available_models()
        return render_template('index.html', models=models)
    
    @app.route('/gallery')
    def gallery():
        """Gallery page showing all generated images"""
        page = request.args.get('page', 1, type=int)
        per_page = 12
        
        images = GeneratedImage.query.order_by(
            GeneratedImage.created_at.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return render_template('gallery.html', images=images)
    
    @app.route('/api/generate', methods=['POST'])
    def api_generate_image():
        """API endpoint for generating images"""
        try:
            data = request.get_json()
            prompt = data.get('prompt', '').strip()
            model_name = data.get('model_name', 'stabilityai/stable-diffusion-2-1')
            
            if not prompt:
                return jsonify({'success': False, 'error': 'Prompt is required'}), 400
            
            if len(prompt) > 1000:
                return jsonify({'success': False, 'error': 'Prompt is too long (max 1000 characters)'}), 400
            
            # Generate unique filename
            filename = f"{uuid.uuid4().hex}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Generate image using Hugging Face API
            success, result = generate_image_from_text(prompt, model_name, filepath)
            
            if not success:
                logger.error(f"Image generation failed: {result}")
                return jsonify({'success': False, 'error': result}), 500
            
            # Get file size
            file_size = os.path.getsize(filepath)
            
            # Save to database
            image_record = GeneratedImage(
                prompt=prompt,
                model_name=model_name,
                filename=filename,
                file_size=file_size
            )
            db.session.add(image_record)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'image_id': image_record.id,
                'filename': filename,
                'download_url': url_for('download_image', filename=filename)
            })
            
        except Exception as e:
            logger.error(f"Error in generate_image: {str(e)}")
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @app.route('/download/<filename>')
    def download_image(filename):
        """Download generated image"""
        try:
            filename = secure_filename(filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if not os.path.exists(filepath):
                return "File not found", 404
            
            return send_file(filepath, as_attachment=True, download_name=filename)
            
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            return "Error downloading file", 500
    
    @app.route('/api/delete/<int:image_id>', methods=['DELETE'])
    def api_delete_image(image_id):
        """API endpoint for deleting images"""
        try:
            image = GeneratedImage.query.get_or_404(image_id)
            
            # Delete file from filesystem
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # Delete from database
            db.session.delete(image)
            db.session.commit()
            
            return jsonify({'success': True})
            
        except Exception as e:
            logger.error(f"Error deleting image: {str(e)}")
            return jsonify({'success': False, 'error': 'Error deleting image'}), 500
    
    @app.route('/api/models')
    def api_get_models():
        """API endpoint to get available models"""
        models = get_available_models()
        return jsonify({'models': models})
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('index.html', error="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('index.html', error="Internal server error"), 500
