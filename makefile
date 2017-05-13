
pythonFile=$(find . -name "*.py")

all: mosaic_fr.ts mosaic_fr.qm 

mosaic_fr.ts: ${pythonFile}
	pylupdate5 mosaic.pro
    
mosaic_fr.qm: mosaic_fr.ts
	/home/nicolas/Qt5.8/5.8/gcc_64/bin/lrelease mosaic.pro
