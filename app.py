from flask import Flask, request, render_template_string, send_from_directory, flash, redirect, url_for
import subprocess
import shutil
import os

app = Flask(__name__)
app.secret_key = 'super secret key'  # Necessary for flash messages

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        git_url = request.form['git_url'].strip()

        # Basic validation of the git_url
        if not git_url or "github.com" not in git_url:
            flash('Invalid URL. Please enter a valid GitHub repository URL.', 'error')
            return redirect(url_for('home'))

        # Attempt to clone and process the repository
        try:
            # Extract the repository name from the URL
            folder_name = git_url.split('/')[-1]
            if folder_name.endswith('.git'):
                folder_name = folder_name[:-4]

            # Ensure the 'done' directory exists
            done_dir = 'done'
            if not os.path.exists(done_dir):
                os.makedirs(done_dir)

            # Execute git clone
            subprocess.check_call(['git', 'clone', git_url], stderr=subprocess.STDOUT)

            # Zip the folder
            shutil.make_archive(folder_name, 'zip', folder_name)

            # Remove the original folder
            shutil.rmtree(folder_name)

            # Move the zip file to the 'done' directory
            shutil.move(f"{folder_name}.zip", done_dir)

            return redirect(url_for('download_page', filename=f"{folder_name}.zip"))
        except subprocess.CalledProcessError:
            flash('Failed to clone repository. Please check the URL and try again.', 'error')

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Git Clone and Zip</title>
        <style>
            body { background-color: black; color: white; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { text-align: center; }
            input[type="text"] { width: 80%; max-width: 500px; padding: 10px; margin-bottom: 20px; border: 2px solid #d00; background-color: #000; color: #fff; }
            .button { background-color: #d00; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
            .button:hover { background-color: #a00; }
            .error { color: #d00; }
            @media (max-width: 600px) {
                input[type="text"] { width: 75%; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Enter GitHub Repository URL</h2>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="error">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            <form action="/" method="post">
                <input type="text" name="git_url" placeholder="https://github.com/username/repository" required>
                <br>
                <button type="submit" class="button">Clone and Zip</button>
            </form>
        </div>
    </body>
    </html>
    """, error=False)

@app.route('/download-page/<filename>')
def download_page(filename):
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Download Ready</title>
        <style>
            body { background-color: black; color: white; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .button { background-color: #d00; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
            .button:hover { background-color: #a00; }
        </style>
    </head>
    <body>
        <div>
            <h2>Your download is ready!</h2>
            <a href="{{ url_for('download_file', filename=filename) }}" class="button">Download ZIP</a>
        </div>
    </body>
    </html>
    """, filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(directory='done', path=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
