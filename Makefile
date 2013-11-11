
help:
	@echo "exe       make shanbay.exe"
	@echo "register  register to pypi"
	@echo "publish   publish to pypi"

exe:
	@echo "make shanbay.exe"
	"e:\Python27\Scripts\pyinstaller.exe" shanbay.spec

publish:
	@echo "publish to pypi"
	python setup.py publish

register:
	@echo "register to pypi"
	python setup.py register
