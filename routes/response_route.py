from flask import request, render_template, redirect, Blueprint
from member import Response, ResponseService

service = ResponseService()

bp = Blueprint('response', __name__, url_prefix='/response')

@bp.route('/add')
def addFormResponse():
    return render_template('response/form.html')

@bp.route('/get')
def getContent():
    num = request.args.get('num', 0, int)
    b = service.getByNum(num)
    return render_template('response/content.html', b=b)

@bp.route('/add', methods=['POST'])
def addResponse():
    resnum = int(request.form['resnum'])
    write = request.form['write']
    service.addResponse(Response(resnum=resnum, write=write))
    return redirect('/board/list')