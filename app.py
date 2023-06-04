from flask import Flask, render_template, request, send_file
from urllib.parse import urlparse, parse_qs
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)

def get_vid_id(url):
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    if(url_data.hostname == 'youtu.be'):
        return url_data.path[1:]
    elif(url_data.hostname in ('www.youtube.com', 'youtube.com')):
        if('v' in query):
            return query['v'][0]
        elif('vi' in query):
            return query['vi'][0]
        else:
            return None
    else:
        return None
    
def get_vid_title(url) :
    yt = YouTube(url)
    return yt.title

def resolve_title(title):
    title = title.replace('|', '')
    title = title.replace('?', '')
    title = title.replace('/', '')
    title = title.replace('\\', '')
    title = title.replace(':', '')
    title = title.replace('*', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('"', '')
    title = title.replace('\'', '')
    title = title.replace('!', '')
    title = title.replace(';', '')
    title = title.replace('(', '')
    title = title.replace(')', '')
    title = title.replace(' ', '_')
    return title

def download_yt(url, format):
    buffer = BytesIO()
    try:
        yt = YouTube(url)
        yt.title = resolve_title(yt.title)
        if(format == 'audio'):
            stream = yt.streams.filter(only_audio=True).first()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, download_name=yt.title, as_attachment=True, mimetype='audio/mp3')
        else:
            # Get the video stream highest resolution
            stream = yt.streams.get_highest_resolution()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, download_name=yt.title, as_attachment=True, mimetype='video/mp4')
            
    except Exception as e:
        print(e)
        return send_file(buffer, download_name="Temp", as_attachment=True)


@app.route('/')
def welcome():
    return render_template('index.html', url='', welcome=True)

@app.route('/get_vid_img', methods=['GET', 'POST'])
def get_vid_img():
    if request.method == 'POST':
        # Get the url from the form
        vid_url = request.form['url']
        print(vid_url)
        vid_id = get_vid_id(vid_url)
        if(not vid_id):
            return render_template('index.html', url='_', vid_found=False)
        # Re-direct to the url_for get_vid_img function
        img_url = 'https://img.youtube.com/vi/' + vid_id + '/0.jpg'
        title = get_vid_title(vid_url)
        return render_template('index.html', url=vid_url, vid_found=True, img_url=img_url, title=title)
    else:
        return render_template('index.html', url='_', vid_found=False)
    
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        vid_url = request.form['url']
        format = request.form['flexRadioDefault']
        
        vid_id = get_vid_id(vid_url)
        # title = get_vid_title(vid_url)
        # img_url = 'https://img.youtube.com/vi/' + vid_id + '/0.jpg'

        return download_yt(vid_url, format)
        # return render_template('index.html', url=vid_url, vid_found=True, img_url=img_url, title=title)

    else :
        return render_template('index.html', url='_', vid_found=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000)