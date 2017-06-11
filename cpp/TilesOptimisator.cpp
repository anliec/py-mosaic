#include "TilesOptimisator.h"
#include <cmath>
#include <climits>

#include <iostream>

const double IMPORTANCE_FACTOR = 100000.0;
const double SHARPNESS_FACTOR = 1.0;
const unsigned MAX_DISTANCE_OPTIMISATION = 3; //max ditance in with the by picture optimisator will work

extern "C" void hello()
{
    std::cout << "Hello World" << std::endl;
}

/**
 * @param tiles input the tiles in 3 dimention (sizeX * sizeY * sizeN)
 *  return a table of pyTiles of size sizeX * sizeY ordered by column first.
 */
extern "C" void python_main(pyTiles * tiles, int sizeX, int sizeY, int sizeN)
{
    TilesOptimisator opt(tiles, sizeX, sizeY, sizeN);
    //opt.basicOptimisator();
    opt.byPictureObtimisator();
    //generate output into the input table "tiles"
    opt.getPyTiles();
}

TilesOptimisator::TilesOptimisator(pyTiles * tiles, int sizeX, int sizeY, int sizeN)
{
    //set the return array as the input one
    retArray = tiles;
    for(int x=0 ; x<sizeX ; x++)
    {
        std::vector<std::pair<sh_Tile, std::multimap<int, sh_Tile>>> xVector;
        unsigned xIndex = x * sizeY * sizeN;
        for(int y=0 ; y<sizeY ; y++)
        {
            std::pair<sh_Tile, std::multimap<int, sh_Tile>> yVector;
            unsigned yIndex = xIndex + y * sizeN;
            for(int n=0 ; n<sizeN ; n++)
            {
                unsigned index = yIndex + n;
                //create a proper Tile
                sh_Tile t = std::make_shared<Tile>();
                t->name = tiles[index].path;
                t->scoreBase = tiles[index].score;
                t->posX = x;
                t->posY = y;
                t->scoreFinal = t->scoreBase;
                //store the tile in the map
                yVector.second.insert(std::pair<int, sh_Tile>(t->scoreBase,t));
            }
            //set the best tile of yVector as the one with the lowest score
            yVector.first = yVector.second.begin()->second;
            //add the vector of y coordinate after the x one
            xVector.push_back(yVector);
            //add the current best to the best tile map
            sh_Tile &bestTile = yVector.first;
            bestTileByNameAndScore[bestTile->name].insert(std::pair<int, sh_Tile>(bestTile->scoreBase, bestTile));
        }
        //add the filled xVector to the final vector
        tilesByPos.push_back(xVector);
    }
//    for(std::vector<std::pair<Tile*, std::multimap<int, Tile>>> vectx : tilesByPos)
//    {
//        for(std::pair<Tile*, std::multimap<int, Tile>> pair : vectx)
//        {
//            std::cout << "best tile : " << pair.first->name << " - " << pair.first->scoreBase
//                      << std::endl << "full tile list :" << std::endl;
//            for(std::pair<int, Tile> tile : pair.second)
//            {
//                std::cout << "\t- " << tile.second.name << " - " << tile.second.scoreBase << std::endl;
//            }
//        }
//    }
}

TilesOptimisator::~TilesOptimisator()
{

}

void TilesOptimisator::basicOptimisator(unsigned numberOfLoop)
{
    for(unsigned loop=0 ; loop<numberOfLoop ; loop++)
    {
        for(unsigned x=0 ; x<tilesByPos.size() ; x++)
        {
            auto tilesAtX = tilesByPos[x];
            for(unsigned y=0 ; y<tilesAtX.size() ; y++)
            {
                lookForBetterTileAtPos(x,y);
            }
        }
    }
}

void TilesOptimisator::byPictureObtimisator()
{
    unsigned currentDepth = 0;
    bool loop = false;
    do
    {
        loop = false;
        for(std::pair<std::string, std::multimap<int, sh_Tile>> sameNameTiles : bestTileByNameAndScore)
        {
            std::multimap<int, sh_Tile> &samenameMap = sameNameTiles.second;
            auto pivoIt = samenameMap.begin();
            //go to the wanted depth
            for(unsigned i=0 ; i<currentDepth && pivoIt!=samenameMap.end() ; ++i)
                pivoIt++;
            if(pivoIt != sameNameTiles.second.end())
            {
                loop = true;
                sh_Tile &pivoTile = pivoIt->second;
                std::multimap<int, sh_Tile> siblingsByDistance = getDistanceToSiblings(pivoTile);
                for(std::pair<int, sh_Tile> siblingPair : siblingsByDistance)
                {
                    if(siblingPair.first > MAX_DISTANCE_OPTIMISATION)
                        break;
                    sh_Tile &sibling = siblingPair.second;
                    lookForBetterTileAtPos(sibling->posX, sibling->posY);
                }
            }
        }
        currentDepth++;
    }while(loop);
}

pyTiles *TilesOptimisator::getPyTiles()
{
    unsigned sizeY = tilesByPos[0].size();

    unsigned x=0, y=0;
    for(std::vector<std::pair<sh_Tile, std::multimap<int, sh_Tile>>> vectx : tilesByPos)
    {
        y=0;
        for(std::pair<sh_Tile, std::multimap<int, sh_Tile>> pair : vectx)
        {
            pyTiles tile;
            tile.path = new char[pair.first->name.length()+1];
            pair.first->name.copy(tile.path, pair.first->name.length());
            tile.path[pair.first->name.length()] = '\0';
            tile.score = pair.first->scoreBase;
            retArray[x*sizeY + y] = tile;
            y++;
        }
        x++;
    }
    return retArray;
}

unsigned TilesOptimisator::tilesDistance(const sh_Tile &A, const sh_Tile &B) const
{
    unsigned distanceX = std::abs(A->posX - B->posX);
    unsigned distanceY = std::abs(A->posY - B->posY);
    return std::max(distanceX, distanceY);
}

int TilesOptimisator::getdistanceToClosestSibling(const sh_Tile &A) const
{
    int clossestSibling = INT_MAX;
    auto it=bestTileByNameAndScore.find(A->name);
    if(it == bestTileByNameAndScore.end())
    {
        std::cout << A->name << " not found in map !" << std::endl;
        return clossestSibling;
    }
    const std::multimap<int, sh_Tile> &siblingTiles = it->second;
    for(std::pair<int, sh_Tile> pair : siblingTiles)
    {
        sh_Tile &tile = pair.second;
        int d = tilesDistance(A,tile);
        if(clossestSibling > d && d != 0)
        {
            clossestSibling = d;
        }
    }
    return clossestSibling;
}

std::multimap<int, sh_Tile> TilesOptimisator::getDistanceToSiblings(const sh_Tile &tile) const
{
    std::multimap<int, sh_Tile> clossestSiblings;
    auto it=bestTileByNameAndScore.find(tile->name);
    if(it == bestTileByNameAndScore.end())
    {
        return clossestSiblings;
    }
    const std::multimap<int, sh_Tile> &siblingTiles = it->second;
    for(std::pair<int, sh_Tile> pair : siblingTiles)
    {
        sh_Tile &currentTile = pair.second;
        int d = tilesDistance(tile,currentTile);
        //add the distance to the return map
        clossestSiblings.insert(std::pair<int, sh_Tile>(d, currentTile));
    }
    return clossestSiblings;
}

unsigned TilesOptimisator::computeAditionnalScore(const sh_Tile &A) const
{
    int d = getdistanceToClosestSibling(A);
    unsigned score = IMPORTANCE_FACTOR * std::exp(-d * SHARPNESS_FACTOR);
    if(d == INT_MAX)
        std::cout << "d max, score is : " << score << std::endl;
    return score;
}

void TilesOptimisator::setFinalScore(sh_Tile &A) const
{
    A->scoreFinal = A->scoreBase + computeAditionnalScore(A);
}

/**
 * @brief TilesOptimisator::setBestPictureAtPos set the best tile at the given position
 * by keeping the internal data structure in a correct state
 * @param x the x coordinate of the new best tile
 * @param y the y coordinate of the new best tile
 * @param tile the tile to set as best picture
 */
void TilesOptimisator::setBestPictureAtPos(unsigned x, unsigned y, sh_Tile &tile)
{
    ///first remove the old best tile from the best tile map
    sh_Tile oldBestTile = tilesByPos[x][y].first;
    std::multimap<int, sh_Tile> &tileMuptimap = bestTileByNameAndScore[oldBestTile->name];
    //select the tiles with the same score on the list
    auto itPair = tileMuptimap.equal_range(oldBestTile->scoreBase);
    //and look in that selection for the rigth Tile to delete
    for(auto it=itPair.first ; it!=itPair.second ; ++it)
    {
        if(it->second == oldBestTile)
        {
            tileMuptimap.erase(it);
            break;
        }
    }
    ///now add the tile to the best tile map
    bestTileByNameAndScore[tile->name].insert(std::pair<int, sh_Tile>(tile->scoreBase, tile));
    tilesByPos[x][y].first = tile;
}

void TilesOptimisator::setBestPictureAtPos(sh_Tile &tile)
{
    setBestPictureAtPos(tile->posX, tile->posY, tile);
}

/**
 * @brief TilesOptimisator::computeAllTopScore compute the score of all the Tiles currantly on top of their position
 * (the less scored tiles at the given position)
 */
void TilesOptimisator::computeAllTopScore()
{
    for(std::vector<std::pair<sh_Tile, std::multimap<int, sh_Tile>>> yTiles : tilesByPos)
    {
        for(std::pair<sh_Tile, std::multimap<int, sh_Tile>> tiles : yTiles)
        {
            sh_Tile t = tiles.first;
            setFinalScore(t);
        }
    }
}

void TilesOptimisator::lookForBetterTileAtPos(unsigned x, unsigned y)
{
    std::pair<sh_Tile, std::multimap<int, sh_Tile>> &caseAtPos = tilesByPos[x][y];
    sh_Tile currentBestTile = caseAtPos.first;
    std::multimap<int, sh_Tile> &possibleTiles = caseAtPos.second;

    setFinalScore(currentBestTile);
    sh_Tile bestTile = currentBestTile;

    for(std::pair<int, sh_Tile> pair : possibleTiles)
    {
        sh_Tile &t = pair.second;
        if(currentBestTile != t)
        {
            if(bestTile->scoreFinal < t->scoreBase)
            {
                //if the base score of the current tile is bigger than the best score (base scroe + something)
                //no need to continue cherching, the folowing tile have bigger score
                break;
            }
            else
            {
                //compute score of t
                setFinalScore(t);
                //if the score is better than the computes score, we set best tile as t
                if(bestTile->scoreFinal > t->scoreFinal)
                {
                    bestTile = t;
                }
            }
        }
    }
    //set the new best tile
    if(currentBestTile != bestTile)
    {
        setBestPictureAtPos(x, y, bestTile);
    }
}

void TilesOptimisator::setRetArray(pyTiles *value)
{
    retArray = value;
}












