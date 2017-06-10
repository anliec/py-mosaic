#ifndef TILESOPTIMISATOR_H
#define TILESOPTIMISATOR_H

#include <map>
#include <vector>
#include <string>
#include <memory>

struct Tile
{
    std::string name;
    int posX;
    int posY;
    int scoreBase;
    int scoreFinal;
};

struct pyTiles{
    char * path;
    int score;
};

typedef std::shared_ptr<Tile> sh_Tile;

class TilesOptimisator
{
public:
    TilesOptimisator(pyTiles *tiles, int sizeX, int sizeY, int sizeN);
    virtual ~TilesOptimisator();

    void basicOptimisator(unsigned numberOfLoop = 1);
    void byPictureObtimisator();
    pyTiles * getPyTiles();

    void setRetArray(pyTiles *value);

protected:
    unsigned tilesDistance(const sh_Tile &A, const sh_Tile &B) const;
    unsigned getdistanceToClosestSibling(const sh_Tile &A) const;
    std::multimap<unsigned, sh_Tile> getDistanceToSiblings(const sh_Tile &tile) const;
    unsigned computeAditionnalScore(const sh_Tile &A) const;
    void setFinalScore(sh_Tile &A) const;

    void setBestPictureAtPos(unsigned x, unsigned y, sh_Tile &tile);
    void setBestPictureAtPos(sh_Tile &tile);

    void computeAllTopScore();
    void lookForBetterTileAtPos(unsigned x, unsigned y);

private:
    std::map<std::string, std::multimap<int, sh_Tile>> bestTileByNameAndScore;
    std::vector<std::vector<std::pair<sh_Tile, std::multimap<int, sh_Tile>>>> tilesByPos;
    pyTiles * retArray;
};

#endif // TILESOPTIMISATOR_H
