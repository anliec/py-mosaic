SOURCES = mosaic.py\
            GUI/DialogPhotos.py\
            GUI/PreviewGraphicView.py\
            GUI/ExplorationWidget.py\
            GUI/SelectionGraphicView.py\
            GUI/MainWindow.py\
            GUI/NewMosaic.py \
            cpp/TilesOptimisator.cpp\
            core/MosaicGenerator.py\
            core/FindPhotos.py\
            core/databaseFiller.py\
            core/PhotosManaging.py\
            core/database.py


FORMS = GUI/dialogphotos.ui\
        GUI/explorationwindows.ui\
        GUI/mainwindow.ui\
        GUI/NewMosaic.ui

TRANSLATIONS = mosaic_fr.ts

CODECFORTR   = UTF-8

CODECFORSRC  = UTF-8

HEADERS += \
    cpp/TilesOptimisator.h
