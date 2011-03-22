#-------------------------------------------------------------------------------
# Copyright (c) 2010 Patrick Mueller
# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license.php
#-------------------------------------------------------------------------------

.PHONY : all build deploy test clean watch help vendor

#-------------------------------------------------------------------------------
all: help

#-------------------------------------------------------------------------------
build: 
	@echo 
	@echo ===========================================================
	@echo building into ./deploy
	@echo ===========================================================
	
	-@chmod -R +w deploy
	@rm -rf deploy
	
	@mkdir -p deploy/css
	@mkdir -p deploy/images
	@mkdir -p deploy/modules
	@mkdir -p deploy/vendor/zepto
	@mkdir -p deploy/vendor/modjewel
	@mkdir -p deploy/vendor/scooj
	@mkdir -p deploy/vendor/underscore
	
	@echo 
	@echo ===========================================================
	@echo copying static files
	@echo ===========================================================
	cp index-mobile.html      deploy/index-nm.html
	cp css/*                  deploy/css
	cp images/*               deploy/images
	cp vendor/zepto/*.js      deploy/vendor/zepto
	cp vendor/modjewel/*.js   deploy/vendor/modjewel
	cp vendor/underscore/*.js deploy/vendor/underscore
	
	@echo 
	@echo ===========================================================
	@echo compiling scoop files to JavaScript
	@echo ===========================================================
	@rm -rf tmp
	@mkdir tmp
	python vendor/scooj/scoopc.py               --out tmp                 modules
	
	@echo 
	@echo ===========================================================
	@echo converting CommonJS modules to Transport/D format
	@echo ===========================================================
	python vendor/modjewel/module2transportd.py --out deploy/modules      tmp
	python vendor/modjewel/module2transportd.py --out deploy/vendor/scooj vendor/scooj
	
	@echo 
	@echo ===========================================================
	@echo building data
	@echo ===========================================================
	python build-html.py < data.txt > deploy/index-nm.html
	
	@echo 
	@echo ===========================================================
	@echo appcache-ing
	@echo ===========================================================
	sed "s/not-a-manifest/manifest/" \
	    < deploy/index-nm.html \
	    > deploy/index.html
	sed "s/<!-- debug -->/<script src='http:\/\/pmuellr.muellerware.org:8081\/target\/target-script.js'><\/script>/" \
	    < deploy/index.html \
	    > deploy/index-debug.html
	cd deploy; \
	    find  . -type f -print | \
	    sed s/^\.\.// | \
	     grep -v "data.txt" | \
	     grep -v "index-nm.html" \
	     > ../tmp/index.manifest.files
	echo "AddType text/cache-manifest .manifest" > deploy/.htaccess
	echo "CACHE MANIFEST"         > deploy/index.manifest
	echo "# `date`"              >> deploy/index.manifest
	echo                         >> deploy/index.manifest
	cat tmp/index.manifest.files >> deploy/index.manifest
	echo                         >> deploy/index.manifest
	
	@chmod -R -w deploy/*
	
	@echo
	
	@growlnotify -m "mwa-fqf2011 build finished" at `date +%H:%M:%S`
    

#-------------------------------------------------------------------------------
deploy:
	@chmod -R +w deploy
	scp -r deploy/* muellerware.org:web/public/mwa-fqf-2011
	@chmod -R -w deploy

#-------------------------------------------------------------------------------
clean:
	@chmod -R +w deploy
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
	@mkdir vendor/zepto
	curl --silent --show-error --output tmp/zepto.zip $(ZEPTO_URL)/zepto-$(ZEPTO_VERSION).zip
	unzip -q tmp/zepto.zip -d tmp
	mv tmp/zepto-$(ZEPTO_VERSION)/dist/zepto.js vendor/zepto/zepto.js
	rm -rf tmp

#-------------------------------------------------------------------------------
vendor-underscore:
	@echo 
	@echo ===========================================================
	@echo downloading underscore
	@echo ===========================================================
	@mkdir  vendor/underscore
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
	@echo "  help     print this help"
	@echo "  build    build the junk"
	@echo "  deploy   copy to the server"
	@echo "  clean    clean up transient goop"
	@echo "  watch    run 'make build' when a file changes"
	@echo "  vendor   get the vendor files"
	@echo
	@echo You will need to run \'make vendor\' before doing a build.
	
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
	
