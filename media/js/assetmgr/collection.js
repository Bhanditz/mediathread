var CollectionList = function (config) {
    var self = this;
    self.template_label = config.template_label;
    self.view_callback = config.view_callback;
    self.create_annotation_thumbs = config.create_annotation_thumbs;
    self.create_asset_thumbs = config.create_asset_thumbs;
    self.project_id = config.project_id;
    self.project_version = config.project_version;
    self.parent = config.parent;
    self.selected_view = config.hasOwnProperty('selectedView') ? config.selectedView : 'Medium';
    self.citable = config.hasOwnProperty('citable') ? config.citable : false;
    
    self.switcher_context = {};
    
    // add some flair to the collection table
    jQuery(self.parent).find(".collection_table").ajaxStart(function () {
        jQuery(this).addClass("ajaxLoading");
    });
    
    jQuery(self.parent).find(".collection_table").ajaxStop(function () {
        jQuery(this).removeClass("ajaxLoading");
    });
    
    jQuery.ajax({
        url: '/site_media/templates/' + config.template + '.mustache?nocache=v2',
        dataType: 'text',
        cache: false, // Chrome && Internet Explorer has aggressive caching policies.
        success: function (text) {
            MediaThread.templates[config.template] = Mustache.template(config.template, text);
            
            var url = null;
            
            // Retrieve the full asset w/annotations from storage
            if (config.view === 'all' || !config.space_owner) {
                url = MediaThread.urls['all-space'](config.tag, null, self.citable);
            } else {
                url = MediaThread.urls['your-space'](config.space_owner, config.tag, null, self.citable);
            }
            
            djangosherd.storage.get({
                    type: 'asset',
                    url: url
                },
                false,
                function (the_records) {
                    self.updateAssets(the_records);
                });
        }
    });
    
    return this;
};

CollectionList.prototype.selectOwner = function (username) {
    var self = this;
    djangosherd.storage.get({
        type: 'asset',
        url: username ? MediaThread.urls['your-space'](username, null, null, self.citable) : MediaThread.urls['all-space'](null, null, self.citable)
    },
    false,
    function (the_records) {
        self.updateAssets(the_records);
    });
    
    return false;
};


CollectionList.prototype.deleteAsset = function (asset_id) {
    var self = this;
    var url = MediaThread.urls['asset-delete'](asset_id);
    return ajaxDelete(null, 'record-' + asset_id, { 'href': url });
};

CollectionList.prototype.deleteAnnotation = function (annotation_id) {
    var self = this;
    var asset_id = jQuery('#annotation-' + annotation_id).parents("div.record").children("input.record").attr("value");
    var url = MediaThread.urls['annotation-delete'](asset_id, annotation_id);
    return ajaxDelete(null, 'annotation-' + annotation_id, { 'href': url });
};

CollectionList.prototype.clearFilter = function (filterName) {
    var self = this;
    var active_tag = null;
    var active_modified = null;
        
    if (filterName === 'tag') {
        active_modified = ('modified' in self.current_records.active_filters) ? self.current_records.active_filters.modified : null;
    } else if (filterName === 'modified') {
        active_tag = ('tag' in self.current_records.active_filters) ? self.current_records.active_filters.tag : null;
    }
    
    djangosherd.storage.get({
        type: 'asset',
        url: self.getSpaceUrl(active_tag, active_modified)
    },
    false,
    function (the_records) {
        self.updateAssets(the_records);
    });
    
    return false;
};

CollectionList.prototype.filterByDate = function (modified) {
    var self = this;
    var active_tag = ('tag' in self.current_records.active_filters) ? self.current_records.active_filters.tag : null;
    djangosherd.storage.get({
        type: 'asset',
        url: self.getSpaceUrl(active_tag, modified)
    },
    false,
    function (the_records) {
        self.updateAssets(the_records);
    });
    
    return false;
};

CollectionList.prototype.filterByTag = function (tag) {
    var self = this;
    var active_modified = ('modified' in self.current_records.active_filters) ? self.current_records.active_filters.modified : null;
    djangosherd.storage.get({
        type: 'asset',
        url: self.getSpaceUrl(tag, active_modified)
    },
    false,
    function (the_records) {
        self.updateAssets(the_records);
    });
    
    return false;
};

CollectionList.prototype.filterByClassTag = function (tag) {
    var self = this;
    djangosherd.storage.get({
        type: 'asset',
        url: MediaThread.urls['all-space'](tag, null, self.citable)
    },
    false,
    function (the_records) {
        self.updateAssets(the_records);
    });
    
    return false;
};

CollectionList.prototype.getShowingAllItems = function (json) {
    return !json.hasOwnProperty('space_owner');
};

CollectionList.prototype.getSpaceUrl = function (active_tag, active_modified) {
    var self = this;
    if (self.getShowingAllItems(self.current_records)) {
        return MediaThread.urls['all-space'](active_tag, active_modified, self.citable);
    } else {
        return MediaThread.urls['your-space'](self.current_records.space_owner.username, active_tag, active_modified, self.citable);
    }
};

CollectionList.prototype.createAssetThumbs = function (assets) {
    var self = this;
    djangosherd.thumbs = [];
    for (var i = 0; i < assets.length; i++) {
        var asset = assets[i];
        DjangoSherd_adaptAsset(asset); //in-place
        
        var target_parent = jQuery(self.parent).find(".gallery-item-" + asset.id)[0];
        
        if (!asset.thumbable) {
            jQuery(target_parent).css({ height: '200px' });
        } else {
            var view;
            switch (asset.type) {
            case 'image':
                view = new Sherd.Image.OpenLayers();
                break;
            case 'fsiviewer':
                view = new Sherd.Image.FSIViewer();
                break;
            }
            djangosherd.thumbs.push(view);
            
            // scale the height
            var width = jQuery(target_parent).width();
            var height = (width / asset.width * asset.height + 65) + 'px';
            jQuery(target_parent).css({ height: height });
            
            var obj_div = document.createElement('div');
            jQuery(target_parent).children('.asset-thumb').append(obj_div);
            
            asset.presentation = 'gallery';
            asset.x = 0;
            asset.y = 0;
            asset.zoom = 1;
            
            view.html.push(obj_div, { asset: asset });
            view.setState(asset);
        }
    }
};

CollectionList.prototype.createThumbs = function (assets) {
    var self = this;
    djangosherd.thumbs = [];
    for (var i = 0; i < assets.length; i++) {
        var asset = assets[i];
        DjangoSherd_adaptAsset(asset); //in-place
        if (asset.thumbable && asset.annotations) {
            for (var j = 0; j < asset.annotations.length; j++) {
                var ann = asset.annotations[j];
                
                var view;
                switch (asset.type) {
                case 'image':
                    view = new Sherd.Image.OpenLayers();
                    break;
                case 'fsiviewer':
                    view = new Sherd.Image.FSIViewer();
                    break;
                }
                djangosherd.thumbs.push(view);
                var obj_div = document.createElement('div');
                obj_div.setAttribute('class', 'annotation-thumb');

                var target_div = jQuery(self.parent).find(".annotation-thumb-" + ann.id)[0];
                target_div.appendChild(obj_div);
                // should probably be in .view
                asset.presentation = 'thumb';

                ann.asset = asset;
                view.html.push(obj_div, ann);
                view.setState(ann.annotation);
            }
        }
    }
};

CollectionList.prototype.updateProject = function () {
    var self = this;
    var url = MediaThread.urls['project-readonly'](self.project_id, self.project_version);
    
    // retrieve project json
    djangosherd.storage.get({
        type: 'project',
        url: url
    },
    false,
    function (json) {
        self.current_project = json.panels[0].context.project;
        self.switcher_context.project = self.current_project;
        self.updateSwitcher();
    });
};

CollectionList.prototype.updateSwitcher = function () {
    var self = this;
    self.switcher_context.display_switcher_extras = !self.switcher_context.showing_my_items || (self.current_project && self.current_project.participants.length > 1);
    Mustache.update("switcher_collection_chooser", self.switcher_context, { parent: self.parent });
    
    // hook up switcher choice owner behavior
    jQuery(self.parent).find("a.switcher-choice.owner").unbind('click').click(function (evt) {
        var srcElement = evt.srcElement || evt.target || evt.originalTarget;
        var bits = srcElement.href.split("/");
        var username = bits[bits.length - 1];
        
        if (username === "all-class-members") {
            username = null;
        }
        return self.selectOwner(username);
    });

};

CollectionList.prototype.getAssets = function () {
    var self = this;
    return jQuery(self.parent).find('.asset-table').get(0);
};

CollectionList.prototype.updateAssets = function (the_records) {
    var self = this;
    self.switcher_context.owners = the_records.owners;
    self.switcher_context.space_viewer = the_records.space_viewer;
    self.switcher_context.selected_view = self.selected_view;
    
    if (self.getShowingAllItems(the_records)) {
        self.switcher_context.selected_label = "All Class Members";
        self.switcher_context.showing_all_items = true;
        self.switcher_context.showing_my_items = false;
        the_records.showing_all_items = true;
    } else if (the_records.space_owner.username === the_records.space_viewer.username) {
        self.switcher_context.selected_label = "Me";
        self.switcher_context.showing_my_items = true;
        self.switcher_context.showing_all_items = false;
        the_records.showing_my_items = true;
    } else {
        self.switcher_context.showing_my_items = false;
        self.switcher_context.showing_all_items = false;
        self.switcher_context.selected_label = the_records.space_owner.public_name;
    }
    
    self.current_records = the_records;
    
    var n = _propertyCount(the_records.active_filters);
    if (n > 0) {
        the_records.active_filter_count = n;
    }
    
    Mustache.update(self.template_label, the_records, {
        parent: self.parent,
        pre: function (elt) { jQuery(elt).hide(); },
        post: function (elt) {
            if (self.create_annotation_thumbs) {
                self.createThumbs(the_records.assets);
            } else if (self.create_asset_thumbs) {
                self.createAssetThumbs(the_records.assets);
            }
            
            if (self.project_id && !self.current_project) {
                self.updateProject();
            } else {
                self.updateSwitcher();
            }
            
            jQuery(elt).fadeIn("slow");
            
            jQuery(self.parent).find("a.switcher-choice.remove").unbind('click').click(function (evt) {
                var href = jQuery(this).attr("href");
                var bits = href.split("/");
                var filterName = bits[bits.length - 1];
                
                if (filterName === "both") {
                    filterName = null;
                }
                return self.clearFilter(filterName);
            });
            
            jQuery(self.parent).find("p.filterbydate a.switcher-choice").unbind('click').click(function (evt) {
                var srcElement = evt.srcElement || evt.target || evt.originalTarget;
                var bits = srcElement.href.split("/");
                var filterName = bits[bits.length - 1];
                
                if (filterName === "both") {
                    filterName = null;
                }
                return self.filterByDate(filterName);
            });

            jQuery(self.parent).find("a.switcher-choice.filterbytag").unbind('click').click(function (evt) {
                var srcElement = evt.srcElement || evt.target || evt.originalTarget;
                var bits = srcElement.href.split("/");
                return self.filterByTag(bits[bits.length - 1]);
            });
            
            jQuery(self.parent).find("a.collection-choice.delete-asset").unbind('click').click(function (evt) {
                var srcElement = evt.srcElement || evt.target || evt.originalTarget;
                var bits = srcElement.parentNode.href.split("/");
                return self.deleteAsset(bits[bits.length - 1]);
            });
            
            jQuery(self.parent).find("a.collection-choice.delete-annotation").unbind('click').click(function (evt) {
                var srcElement = evt.srcElement || evt.target || evt.originalTarget;
                var bits = srcElement.parentNode.href.split("/");
                return self.deleteAnnotation(bits[bits.length - 1]);
            });
            
            if (self.view_callback) {
                self.view_callback();
            }
            
            jQuery(window).trigger("resize");
        }
    });
};
    