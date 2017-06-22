from minifw.core import framewk


@framewk.get('/')
async def index(request):
    return {
        '__template__': 'test.html',
    }