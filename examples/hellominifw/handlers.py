from minifw.core import framewk


@framewk.get('/')
async def index(request):
    #users = await User.find_all()
    return {
        '__template__': 'test.html',
        'users': None
    }