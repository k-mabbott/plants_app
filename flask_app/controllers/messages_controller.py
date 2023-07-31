
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_app.models.message_model import Message
from flask import request   
 


@app.route('/create/message/<int:id>', methods=['POST'])
def create_message(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        **request.form,
        'recipient_id': id,
        'sender_id': session['user_id']
    }
    Message.save(data)
    return redirect('/dashboard')


@app.route('/message/delete/<int:id>')
def delete_message(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    message_to_delete = Message.get_by_id(data)
    if session['user_id'] != message_to_delete.recipient_id:
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)  
        return render_template('warn.html', message = message_to_delete, ip=ip)
    Message.destroy(data)
    return redirect('/dashboard')

@app.route('/warning')
def warn_user():

    return render_template('warn.html')





# const formatDuration = ms => {
#   if (ms < 0) ms = -ms;
#   const time = {
#     // Add rows here to divide & mod by the # of milliseconds per week, per month & per year approx
#     day: Math.floor(ms / 86400000),
#     hour: Math.floor(ms / 3600000) % 24,
#     minute: Math.floor(ms / 60000) % 60,
#     second: Math.floor(ms / 1000) % 60,
#     millisecond: Math.floor(ms) % 1000
#   };
#   // here set the array to a 'results' string rather than returning immediately
#   return Object.entries(time)
#     .filter(val => val[1] !== 0)
#     .map(([key, val]) => `${val} ${key}${val !== 1 ? 's' : ''}`)
#     .join(', ');
#   // Then just return the front slice from zero to the first comma in the string
# };