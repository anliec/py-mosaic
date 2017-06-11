
pythonFile=$(find . -name "*.py")
BIN=dist/mosaic/mosaic

dist: ${BIN}

dist-win: ${pythonFile} mosaic.pro mosaic_fr.qm cpp/TilesOptimisatorlib.dll
	@pyinstaller mosaic.py --add-binary ./cpp/TilesOptimisatorlib.dll:cpp --add-binary ./mosaic_fr.qm:.

${BIN}: ${pythonFile} mosaic.pro mosaic_fr.qm cpp/TilesOptimisatorlib.so
	@pyinstaller mosaic.py --add-binary ./cpp/TilesOptimisatorlib.so:cpp --add-binary ./mosaic_fr.qm:.

cpp/TilesOptimisatorlib.so: cpp/TilesOptimisator.cpp cpp/TilesOptimisator.h
	@g++ -shared -o $@ -fPIC $< -O3 -Wall
	
cpp/TilesOptimisatorlib.dll: TilesOptimisator.cpp TilesOptimisator.h
	@g++ -shared -o $@ -fPIC $< -O3 -Wall

lang: mosaic_fr.ts mosaic_fr.qm 

mosaic_fr.ts: ${pythonFile} mosaic.pro
	@pylupdate5 mosaic.pro
    
mosaic_fr.qm: mosaic_fr.ts
	@/home/nicolas/Qt5.8/5.8/gcc_64/bin/lrelease mosaic.pro
