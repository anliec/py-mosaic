
lib: TilesOptimisatorlib.so

lib-win: TilesOptimisatorlib.dll

TilesOptimisatorlib.so: TilesOptimisator.cpp TilesOptimisator.h
	@g++ -shared -o $@ -fPIC $< -O3 -Wall
	
TilesOptimisatorlib.dll: TilesOptimisator.cpp TilesOptimisator.h
	@g++ -shared -o $@ -fPIC $< -O3 -Wall
