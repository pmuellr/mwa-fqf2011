#-------------------------------------------------------------------------------
# Copyright (c) 2010 Patrick Mueller
# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license.php
#-------------------------------------------------------------------------------

.PHONY : all build test clean watch vendor help

#-------------------------------------------------------------------------------

all: help

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------

build:

	@echo
	@echo ----------------------------------
	@echo Building
	@echo ----------------------------------
	
	-@chmod -R +w deploy/*
	@rm -rf deploy
	
	@mkdir -p deploy/images/gcons
	@mkdir -p deploy/css
	@mkdir -p deploy/modules
	@mkdir -p deploy/vendor/jo/js
	@mkdir -p deploy/vendor/jo/css
	@mkdir -p deploy/vendor/jquery
	@mkdir -p deploy/vendor/jquery.mobile/images
	@mkdir -p deploy/vendor/modjewel
	@mkdir -p deploy/vendor/scooj
	
	@cp index-mobile.html                            deploy/index.html
	@cp css/*                                        deploy/css
	@cp images/*.jpg                                 deploy/images
	@cp images/*.png                                 deploy/images
	@cp images/gcons/*.png                           deploy/images/gcons
	@cp vendor/jo/js/jo_min.js                       deploy/vendor/jo/js
	@cp vendor/jo/js/jo.js                           deploy/vendor/jo/js
	@cp vendor/jo/css/*.css                          deploy/vendor/jo/css
	@cp vendor/jo/css/*.png                          deploy/vendor/jo/css
	@cp vendor/jquery/*.js                           deploy/vendor/jquery
	@cp vendor/jquery.mobile/jquery.mobile-1.0a3.js  deploy/vendor/jquery.mobile
	@cp vendor/jquery.mobile/jquery.mobile-1.0a3.css deploy/vendor/jquery.mobile
	@cp vendor/jquery.mobile/images/*.png            deploy/vendor/jquery.mobile/images
	@cp vendor/modjewel/*.js                         deploy/vendor/modjewel
	
	@rm -rf tmp
	@mkdir tmp
	
	@python vendor/scooj/scoopc.py               --out tmp                 modules
	@python vendor/modjewel/module2transportd.py --out deploy/modules      tmp
	@python vendor/modjewel/module2transportd.py --out deploy/vendor/scooj vendor/scooj
	
	@chmod -R -w deploy/*
	
	@echo

#-------------------------------------------------------------------------------
clean:

	rm -rf tmp
	rm -rf build
	rm -rf vendor

#-------------------------------------------------------------------------------
watch:

	@run-when-changed "make build" *

#-------------------------------------------------------------------------------

vendor:
	@rm -rf vendor
	
	@mkdir vendor
	
	@rm -rf tmp
	@mkdir tmp
	@mkdir vendor/jo
	curl -o tmp/jo.zip $(JO_URL)/jo-$(JO_VERSION).zip
	unzip tmp/jo.zip -d tmp
	mv tmp/jo-$(JO_VERSION)/* vendor/jo
	rm -rf tmp

	@mkdir  vendor/jquery
	curl -o vendor/jquery/jquery-$(JQUERY_VERSION).min.js  $(JQUERY_URL)/jquery-$(JQUERY_VERSION).min.js
	
	@rm -rf tmp
	@mkdir tmp
	curl --o tmp/jquery.mobile.zip $(JQUERY_MOBILE_URL)/$(JQUERY_MOBILE_VERSION)/jquery.mobile-$(JQUERY_MOBILE_VERSION).zip
	unzip tmp/jquery.mobile.zip -d tmp
	mv tmp/jquery.mobile-1.0a3 vendor/jquery.mobile
	rm -rf tmp
    
	@mkdir  vendor/modjewel
	curl -o vendor/modjewel/modjewel-require.js  $(MODJEWEL_URL)/$(MODJEWEL_VERSION)/modjewel-require.js 
	curl -o vendor/modjewel/module2transportd.py $(MODJEWEL_URL)/$(MODJEWEL_VERSION)/module2transportd.py

	@mkdir  vendor/scooj
	curl -o vendor/scooj/scooj.js  $(SCOOJ_URL)/$(SCOOJ_VERSION)/scooj.js
	curl -o vendor/scooj/scoopc.py $(SCOOJ_URL)/$(SCOOJ_VERSION)/scoopc.py

	mkdir   vendor/run-when-changed
	curl -o vendor/run-when-changed/run-when-changed.py $(RUN_WHEN_CHANGED_URL)


#-------------------------------------------------------------------------------

help:

	@echo make targets available:
	@echo \  help
	@echo \  build
	@echo \  deploy-local
	@echo \  clean
	@echo \  watch
	@echo \  vendor
	
#-------------------------------------------------------------------------------

LOCAL_DEPLOY           = ~/Sites/Public/mwa-fqf2011

MODJEWEL_URL           = https://github.com/pmuellr/modjewel/raw
MODJEWEL_VERSION       = master

SCOOJ_URL              = https://github.com/pmuellr/scooj/raw
SCOOJ_VERSION          = master

UNDERSCORE_URL         = https://github.com/documentcloud/underscore/raw
UNDERSCORE_VERSION     = 1.1.3

BACKBONE_URL           = https://github.com/documentcloud/backbone/raw
BACKBONE_VERSION       = 0.3.3

JQUERY_URL             = http://code.jquery.com
JQUERY_VERSION         = 1.5

JQUERY_MOBILE_URL      = http://code.jquery.com/mobile
JQUERY_MOBILE_VERSION  = 1.0a3

QUNIT_URL              = https://github.com/jquery/qunit/raw
QUNIT_VERSION          = master

RUN_WHEN_CHANGED_URL   = https://gist.github.com/raw/240922/0f5bedfc42b3422d0dee81fb794afde9f58ed1a6/run-when-changed.py

JO_URL                 = http://joapp.com/forums/index.php?p=/discussion/download/6
JO_VERSION             = 0.4.1
JO_URL_GH              = http://cloud.github.com/downloads/davebalmer/jo
	
