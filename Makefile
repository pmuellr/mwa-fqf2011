#-------------------------------------------------------------------------------
# Copyright (c) 2010 Patrick Mueller
# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license.php
#-------------------------------------------------------------------------------

.PHONY : all build test clean watch help vendor

#-------------------------------------------------------------------------------
all: help

#-------------------------------------------------------------------------------
build:
	@echo 
	@echo ===========================================================
	@echo building into ./deploy
	@echo ===========================================================
	
	-@chmod -R +w deploy/*
	@rm -rf deploy
	
	@mkdir -p deploy/images/gcons
	@mkdir -p deploy/css
	@mkdir -p deploy/modules
	@mkdir -p deploy/vendor/zepto
	@mkdir -p deploy/vendor/modjewel
	@mkdir -p deploy/vendor/scooj
	@mkdir -p deploy/vendor/underscore
	
	@cp index-mobile.html      deploy/index.html
	@cp css/*                  deploy/css
	@cp images/*.jpg           deploy/images
	@cp images/*.png           deploy/images
	@cp images/gcons/*.png     deploy/images/gcons
	@cp vendor/zepto/*.js      deploy/vendor/zepto
	@cp vendor/modjewel/*.js   deploy/vendor/modjewel
	@cp vendor/underscore/*.js deploy/vendor/underscore
	
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
	rm -rf deploy
	rm -rf vendor

#-------------------------------------------------------------------------------
watch: build
	@python vendor/run-when-changed/run-when-changed.py "make build" *

#-------------------------------------------------------------------------------
vendor: vendor-prep \
        vendor-modjewel \
        vendor-scoop \
        vendor-run-when-changed \
        vendor-zepto \
        vendor-underscore

#-------------------------------------------------------------------------------
vendor-prep:
	@echo 
	@echo ===========================================================
	@echo getting vendor files
	@echo ===========================================================
	@rm -rf vendor
	@mkdir vendor

#-------------------------------------------------------------------------------
vendor-jo:
	@echo 
	@echo ===========================================================
	@echo downloading jo
	@echo ===========================================================
	@rm -rf tmp
	@mkdir tmp
	@mkdir vendor/jo
	curl --silent --show-error --output tmp/jo.zip $(JO_URL)/jo-$(JO_VERSION).zip
	unzip -q tmp/jo.zip -d tmp
	mv tmp/jo-$(JO_VERSION)/* vendor/jo
	rm -rf tmp

#-------------------------------------------------------------------------------
vendor-zepto:
	@echo 
	@echo ===========================================================
	@echo downloading zepto
	@echo ===========================================================
	@rm -rf tmp
	@mkdir tmp
	curl --silent --show-error --output tmp/zepto.zip $(ZEPTO_URL)/zepto-$(ZEPTO_VERSION).zip
	unzip -q tmp/zepto.zip -d tmp
	mv tmp/zepto-$(ZEPTO_VERSION)/dist vendor/zepto
	rm -rf tmp

#-------------------------------------------------------------------------------
vendor-underscore:
	@echo 
	@echo ===========================================================
	@echo downloading underscore
	@echo ===========================================================
	@mkdir  vendor/underscore
	curl --silent --show-error --output vendor/underscore/underscore-min.js  $(UNDERSCORE_URL)/underscore-min.js
	curl --silent --show-error --output vendor/underscore/underscore.js      $(UNDERSCORE_URL)/underscore.js

#-------------------------------------------------------------------------------
vendor-jquery:
	@echo 
	@echo ===========================================================
	@echo downloading jquery
	@echo ===========================================================
	@mkdir  vendor/jquery
	curl --silent --show-error --output vendor/jquery/jquery-$(JQUERY_VERSION).min.js  $(JQUERY_URL)/jquery-$(JQUERY_VERSION).min.js

#-------------------------------------------------------------------------------
vendor-jquery-mobile:
	@echo 
	@echo ===========================================================
	@echo downloading jquery mobile
	@echo ===========================================================
	@rm -rf tmp
	@mkdir tmp
	curl --silent --show-error --output tmp/jquery.mobile.zip $(JQUERY_MOBILE_URL)/$(JQUERY_MOBILE_VERSION)/jquery.mobile-$(JQUERY_MOBILE_VERSION).zip
	unzip -q tmp/jquery.mobile.zip -d tmp
	mv tmp/jquery.mobile-1.0a3 vendor/jquery.mobile
	rm -rf tmp

#-------------------------------------------------------------------------------
vendor-modjewel:
	@echo 
	@echo ===========================================================
	@echo downloading modjewel
	@echo ===========================================================
	@mkdir  vendor/modjewel
	curl --silent --show-error --output vendor/modjewel/modjewel-require.js  $(MODJEWEL_URL)/$(MODJEWEL_VERSION)/modjewel-require.js 
	curl --silent --show-error --output vendor/modjewel/module2transportd.py $(MODJEWEL_URL)/$(MODJEWEL_VERSION)/module2transportd.py

#-------------------------------------------------------------------------------
vendor-scoop:
	@echo 
	@echo ===========================================================
	@echo downloading scoop
	@echo ===========================================================
	@mkdir  vendor/scooj
	curl --silent --show-error --output vendor/scooj/scooj.js  $(SCOOJ_URL)/$(SCOOJ_VERSION)/scooj.js
	curl --silent --show-error --output vendor/scooj/scoopc.py $(SCOOJ_URL)/$(SCOOJ_VERSION)/scoopc.py

#-------------------------------------------------------------------------------
vendor-run-when-changed:
	@echo 
	@echo ===========================================================
	@echo downloading run-when-changed
	@echo ===========================================================
	mkdir   vendor/run-when-changed
	curl --silent --show-error --output vendor/run-when-changed/run-when-changed.py $(RUN_WHEN_CHANGED_URL)

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

ZEPTO_URL              = http://zeptojs.com/downloads/
ZEPTO_VERSION          = 0.5

UNDERSCORE_URL         = http://documentcloud.github.com/underscore/
UNDERSCORE_VERSION     = 1.1.4

RUN_WHEN_CHANGED_URL   = https://gist.github.com/raw/240922/0f5bedfc42b3422d0dee81fb794afde9f58ed1a6/run-when-changed.py

JO_URL                 = http://joapp.com/forums/index.php?p=/discussion/download/6
JO_VERSION             = 0.4.1
JO_URL_GH              = http://cloud.github.com/downloads/davebalmer/jo
	
