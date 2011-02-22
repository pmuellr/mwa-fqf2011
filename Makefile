#-------------------------------------------------------------------------------
# Copyright (c) 2010 Patrick Mueller
# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license.php
#-------------------------------------------------------------------------------

.PHONY : all build test clean watch vendor help

#-------------------------------------------------------------------------------

all: help

#-------------------------------------------------------------------------------

build:

	@rm -rf tmp
	@mkdir tmp
	
	@echo
	@echo ----------------------------------
	@echo Building
	@echo ----------------------------------
#	cp -R test-cases/* tmp
#	./scoopc.py --out tmp test-cases

#-------------------------------------------------------------------------------

deploy-local: build

	@echo
	@echo ----------------------------------
	@echo Deploying locally
	@echo ----------------------------------
	
	rm -rf deploy
	mkdir deploy
	mkdir deploy/images
	
	cp index-mobile.html deploy/index.html
	cp mwa-fqf2011.css deploy
	cp images/* deploy/images

#-------------------------------------------------------------------------------
clean:

	rm -rf tmp
	rm -rf build
	rm -rf vendor

#-------------------------------------------------------------------------------
watch:

	# from: https://gist.github.com/240922
	run-when-changed "make deploy-local" *

#-------------------------------------------------------------------------------

vendor:
	@rm -rf vendor
	
	@mkdir vendor
	
	@mkdir vendor/jo
	@rm -rf tmp
	@mkdir tmp
	curl --o tmp/jo.zip $(JO_URL)/jo-$(JO_VERSION).zip
	unzip tmp/jo.zip -d tmp
	mv tmp/jo-$(JO_VERSION)/* vendor/jo
	rm -rf tmp

	@rm -rf tmp
	@mkdir tmp
	curl --o tmp/jquery.mobile.zip $(JQUERY_MOBILE_URL)/$(JQUERY_MOBILE_VERSION)/jquery.mobile-$(JQUERY_MOBILE_VERSION).zip
	unzip tmp/jquery.mobile.zip -d tmp
	mv tmp/jquery.mobile-1.0a3 vendor/jquery.mobile
	rm -rf tmp
    
	@mkdir vendor/modjewel
	curl -o vendor/modjewel/modjewel-require.js  $(MODJEWEL_URL)/$(MODJEWEL_VERSION)/modjewel-require.js 
	curl -o vendor/modjewel/module2transportd.py $(MODJEWEL_URL)/$(MODJEWEL_VERSION)/module2transportd.py

	@mkdir vendor/scooj
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
JQUERY_VERSION         = 1.4.4

JQUERY_MOBILE_URL      = http://code.jquery.com/mobile
JQUERY_MOBILE_VERSION  = 1.0a3

QUNIT_URL              = https://github.com/jquery/qunit/raw
QUNIT_VERSION          = master

RUN_WHEN_CHANGED_URL   = https://gist.github.com/raw/240922/0f5bedfc42b3422d0dee81fb794afde9f58ed1a6/run-when-changed.py

JO_URL                 = http://cloud.github.com/downloads/davebalmer/jo
JO_VERSION             = 0.4.0
	
