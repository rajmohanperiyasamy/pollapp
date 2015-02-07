(function (a) {
    "use strict";
    a.widget("blueimp.fileupload", {
        options: {
            namespace: undefined,
            dropZone: a(document),
            fileInput: undefined,
            replaceFileInput: true,
            paramName: undefined,
            singleFileUploads: true,
            sequentialUploads: false,
            forceIframeTransport: false,
            multipart: true,
            maxChunkSize: undefined,
            uploadedBytes: undefined,
            recalculateProgress: true,
            formData: function (a) {
                return a.serializeArray()
            },
            add: function (a, b) {
                b.submit()
            },
            processData: false,
            contentType: false,
            cache: false
        },
        _refreshOptionsList: ["namespace", "dropZone", "fileInput"],
        _isXHRUpload: function (a) {
            var b = "undefined";
            return !a.forceIframeTransport && typeof XMLHttpRequestUpload !== b && typeof File !== b && (!a.multipart || typeof FormData !== b)
        },
        _getFormData: function (b) {
            var c;
            if (typeof b.formData === "function") {
                return b.formData(b.form)
            } else if (a.isArray(b.formData)) {
                return b.formData
            } else if (b.formData) {
                c = [];
                a.each(b.formData, function (a, b) {
                    c.push({
                        name: a,
                        value: b
                    })
                });
                return c
            }
            return []
        },
        _getTotal: function (b) {
            var c = 0;
            a.each(b, function (a, b) {
                c += b.size || 1
            });
            return c
        },
        _onProgress: function (a, b) {
            if (a.lengthComputable) {
                var c = b.total || this._getTotal(b.files),
                    d = parseInt(a.loaded / a.total * (b.chunkSize || c), 10) + (b.uploadedBytes || 0);
                this._loaded += d - (b.loaded || b.uploadedBytes || 0);
                b.lengthComputable = true;
                b.loaded = d;
                b.total = c;
                this._trigger("progress", a, b);
                this._trigger("progressall", a, {
                    lengthComputable: true,
                    loaded: this._loaded,
                    total: this._total
                })
            }
        },
        _initProgressListener: function (b) {
            var c = this,
                d = b.xhr ? b.xhr() : a.ajaxSettings.xhr();
            if (d.upload && d.upload.addEventListener) {
                d.upload.addEventListener("progress", function (a) {
                    c._onProgress(a, b)
                }, false);
                b.xhr = function () {
                    return d
                }
            }
        },
        _initXHRData: function (b) {
            var c, d = b.files[0];
            if (!b.multipart || b.blob) {
                b.headers = a.extend(b.headers, {
                    "X-File-Name": d.name,
                    "X-File-Type": d.type,
                    "X-File-Size": d.size
                });
                if (!b.blob) {
                    b.contentType = d.type;
                    b.data = d
                } else if (!b.multipart) {
                    b.contentType = "application/octet-stream";
                    b.data = b.blob
                }
            }
            if (b.multipart && typeof FormData !== "undefined") {
                if (b.formData instanceof FormData) {
                    c = b.formData
                } else {
                    c = new FormData;
                    a.each(this._getFormData(b), function (a, b) {
                        c.append(b.name, b.value)
                    })
                }
                if (b.blob) {
                    c.append(b.paramName, b.blob)
                } else {
                    a.each(b.files, function (a, d) {
                        if (d instanceof Blob) {
                            c.append(b.paramName, d)
                        }
                    })
                }
                b.data = c
            }
            b.blob = null
        },
        _initIframeSettings: function (a) {
            a.dataType = "iframe " + (a.dataType || "");
            a.formData = this._getFormData(a)
        },
        _initDataSettings: function (a) {
            if (this._isXHRUpload(a)) {
                if (!this._chunkedUpload(a, true)) {
                    if (!a.data) {
                        this._initXHRData(a)
                    }
                    this._initProgressListener(a)
                }
            } else {
                this._initIframeSettings(a)
            }
        },
        _initFormSettings: function (b) {
            if (!b.form || !b.form.length) {
                b.form = a(b.fileInput.prop("form"))
            }
            if (!b.paramName) {
                b.paramName = b.fileInput.prop("name") || "files[]"
            }
            if (!b.url) {
                b.url = b.form.prop("action") || location.href
            }
            b.type = (b.type || b.form.prop("method") || "").toUpperCase();
            if (b.type !== "POST" && b.type !== "PUT") {
                b.type = "POST"
            }
        },
        _getAJAXSettings: function (b) {
            var c = a.extend({}, this.options, b);
            this._initFormSettings(c);
            this._initDataSettings(c);
            return c
        },
        _enhancePromise: function (a) {
            a.success = a.done;
            a.error = a.fail;
            a.complete = a.always;
            return a
        },
        _getXHRPromise: function (b, c, d) {
            var e = a.Deferred(),
                f = e.promise();
            c = c || this.options.context || f;
            if (b === true) {
                e.resolveWith(c, d)
            } else if (b === false) {
                e.rejectWith(c, d)
            }
            f.abort = e.promise;
            return this._enhancePromise(f)
        },
        _chunkedUpload: function (b, c) {
            var d = this,
                e = b.files[0],
                f = e.size,
                g = b.uploadedBytes = b.uploadedBytes || 0,
                h = b.maxChunkSize || f,
                i = e.webkitSlice || e.mozSlice || e.slice,
                j, k, l, m;
            if (!(this._isXHRUpload(b) && i && (g || h < f)) || b.data) {
                return false
            }
            if (c) {
                return true
            }
            if (g >= f) {
                e.error = "uploadedBytes";
                return this._getXHRPromise(false)
            }
            k = Math.ceil((f - g) / h);
            j = function (c) {
                if (!c) {
                    return d._getXHRPromise(true)
                }
                return j(c -= 1).pipe(function () {
                    var f = a.extend({}, b);
                    f.blob = i.call(e, g + c * h, g + (c + 1) * h);
                    f.chunkSize = f.blob.size;
                    d._initXHRData(f);
                    d._initProgressListener(f);
                    l = (a.ajax(f) || d._getXHRPromise(false, f.context)).done(function () {
                        if (!f.loaded) {
                            d._onProgress(a.Event("progress", {
                                lengthComputable: true,
                                loaded: f.chunkSize,
                                total: f.chunkSize
                            }), f)
                        }
                        b.uploadedBytes = f.uploadedBytes += f.chunkSize
                    });
                    return l
                })
            };
            m = j(k);
            m.abort = function () {
                return l.abort()
            };
            return this._enhancePromise(m)
        },
        _beforeSend: function (a, b) {
            if (this._active === 0) {
                this._trigger("start")
            }
            this._active += 1;
            this._loaded += b.uploadedBytes || 0;
            this._total += this._getTotal(b.files)
        },
        _onDone: function (b, c, d, e) {
            if (!this._isXHRUpload(e)) {
                this._onProgress(a.Event("progress", {
                    lengthComputable: true,
                    loaded: 1,
                    total: 1
                }), e)
            }
            e.result = b;
            e.textStatus = c;
            e.jqXHR = d;
            this._trigger("done", null, e)
        },
        _onFail: function (a, b, c, d) {
            d.jqXHR = a;
            d.textStatus = b;
            d.errorThrown = c;
            this._trigger("fail", null, d);
            if (d.recalculateProgress) {
                this._loaded -= d.loaded || d.uploadedBytes || 0;
                this._total -= d.total || this._getTotal(d.files)
            }
        },
        _onAlways: function (a, b, c, d, e) {
            this._active -= 1;
            e.result = a;
            e.textStatus = b;
            e.jqXHR = c;
            e.errorThrown = d;
            this._trigger("always", null, e);
            if (this._active === 0) {
                this._trigger("stop");
                this._loaded = this._total = 0
            }
        },
        _onSend: function (b, c) {
            var d = this,
                e, f, g = d._getAJAXSettings(c),
                h = function (c, f) {
                    e = e || (c !== false && d._trigger("send", b, g) !== false && (d._chunkedUpload(g) || a.ajax(g)) || d._getXHRPromise(false, g.context, f)).done(function (a, b, c) {
                        d._onDone(a, b, c, g)
                    }).fail(function (a, b, c) {
                        d._onFail(a, b, c, g)
                    }).always(function (a, b, c) {
                        if (c && c.done) {
                            d._onAlways(a, b, c, undefined, g)
                        } else {
                            d._onAlways(undefined, b, a, c, g)
                        }
                    });
                    return e
                };
            this._beforeSend(b, g);
            if (this.options.sequentialUploads) {
                f = this._sequence = this._sequence.pipe(h, h);
                f.abort = function () {
                    if (!e) {
                        return h(false, [undefined, "abort", "abort"])
                    }
                    return e.abort()
                };
                return this._enhancePromise(f)
            }
            return h()
        },
        _onAdd: function (b, c) {
            var d = this,
                e = true,
                f = a.extend({}, this.options, c);
            if (f.singleFileUploads && this._isXHRUpload(f)) {
                a.each(c.files, function (f, g) {
                    var h = a.extend({}, c, {
                        files: [g]
                    });
                    h.submit = function () {
                        return d._onSend(b, h)
                    };
                    return e = d._trigger("add", b, h)
                });
                return e
            } else if (c.files.length) {
                c = a.extend({}, c);
                c.submit = function () {
                    return d._onSend(b, c)
                };
                return this._trigger("add", b, c)
            }
        },
        _normalizeFile: function (a, b) {
            if (b.name === undefined && b.size === undefined) {
                b.name = b.fileName;
                b.size = b.fileSize
            }
        },
        _replaceFileInput: function (b) {
            var c = b.clone(true);
            a("<form></form>").append(c)[0].reset();
            b.after(c).detach();
            this.options.fileInput = this.options.fileInput.map(function (a, d) {
                if (d === b[0]) {
                    return c[0]
                }
                return d
            })
        },
        _onChange: function (b) {
            var c = b.data.fileupload,
                d = {
                    files: a.each(a.makeArray(b.target.files), c._normalizeFile),
                    fileInput: a(b.target),
                    form: a(b.target.form)
                };
            if (!d.files.length) {
                d.files = [{
                    name: b.target.value.replace(/^.*\\/, "")
                }]
            }
            if (d.form.length) {
                d.fileInput.data("blueimp.fileupload.form", d.form)
            } else {
                d.form = d.fileInput.data("blueimp.fileupload.form")
            }
            if (c.options.replaceFileInput) {
                c._replaceFileInput(d.fileInput)
            }
            if (c._trigger("change", b, d) === false || c._onAdd(b, d) === false) {
                return false
            }
        },
        _onDrop: function (b) {
            var c = b.data.fileupload,
                d = b.dataTransfer = b.originalEvent.dataTransfer,
                e = {
                    files: a.each(a.makeArray(d && d.files), c._normalizeFile)
                };
            if (c._trigger("drop", b, e) === false || c._onAdd(b, e) === false) {
                return false
            }
            b.preventDefault()
        },
        _onDragOver: function (a) {
            var b = a.data.fileupload,
                c = a.dataTransfer = a.originalEvent.dataTransfer;
            if (b._trigger("dragover", a) === false) {
                return false
            }
            if (c) {
                c.dropEffect = c.effectAllowed = "copy"
            }
            a.preventDefault()
        },
        _initEventHandlers: function () {
            var a = this.options.namespace || this.name;
            this.options.dropZone.bind("dragover." + a, {
                fileupload: this
            }, this._onDragOver).bind("drop." + a, {
                fileupload: this
            }, this._onDrop);
            this.options.fileInput.bind("change." + a, {
                fileupload: this
            }, this._onChange)
        },
        _destroyEventHandlers: function () {
            var a = this.options.namespace || this.name;
            this.options.dropZone.unbind("dragover." + a, this._onDragOver).unbind("drop." + a, this._onDrop);
            this.options.fileInput.unbind("change." + a, this._onChange)
        },
        _beforeSetOption: function (a, b) {
            this._destroyEventHandlers()
        },
        _afterSetOption: function (b, c) {
            var d = this.options;
            if (!d.fileInput) {
                d.fileInput = a()
            }
            if (!d.dropZone) {
                d.dropZone = a()
            }
            this._initEventHandlers()
        },
        _setOption: function (b, c) {
            var d = a.inArray(b, this._refreshOptionsList) !== -1;
            if (d) {
                this._beforeSetOption(b, c)
            }
            a.Widget.prototype._setOption.call(this, b, c);
            if (d) {
                this._afterSetOption(b, c)
            }
        },
        _create: function () {
            var b = this.options;
            if (b.fileInput === undefined) {
                b.fileInput = this.element.is("input:file") ? this.element : this.element.find("input:file")
            } else if (!b.fileInput) {
                b.fileInput = a()
            }
            if (!b.dropZone) {
                b.dropZone = a()
            }
            this._sequence = this._getXHRPromise(true);
            this._active = this._loaded = this._total = 0;
            this._initEventHandlers()
        },
        destroy: function () {
            this._destroyEventHandlers();
            a.Widget.prototype.destroy.call(this)
        },
        enable: function () {
            a.Widget.prototype.enable.call(this);
            this._initEventHandlers()
        },
        disable: function () {
            this._destroyEventHandlers();
            a.Widget.prototype.disable.call(this)
        },
        add: function (b) {
            if (!b || this.options.disabled) {
                return
            }
            b.files = a.each(a.makeArray(b.files), this._normalizeFile);
            this._onAdd(null, b)
        },
        send: function (b) {
            if (b && !this.options.disabled) {
                b.files = a.each(a.makeArray(b.files), this._normalizeFile);
                if (b.files.length) {
                    return this._onSend(null, b)
                }
            }
            return this._getXHRPromise(false, b && b.context)
        }
    })
})(jQuery);
(function (a) {
    "use strict";
    a.widget("blueimpUI.fileupload", a.blueimp.fileupload, {
        options: {
            autoUpload: false,
            sequentialUploads: true,
            maxNumberOfFiles: undefined,
            maxFileSize: 5242880,
            minFileSize: 1,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            previewFileTypes: /^image\/(gif|jpeg|png)$/,
            previewMaxWidth: 80,
            previewMaxHeight: 80,
            previewRequired: false,
            previewAsCanvas: true,
            uploadTemplate: a("#template-upload"),
            downloadTemplate: a("#template-download"),
            dataType: "json",
            add: function (b, c) {
                var d = a(this).data("fileupload");
                d._adjustMaxNumberOfFiles(-c.files.length);
                c.isAdjusted = true;
                c.isValidated = d._validate(c.files);
                c.context = d._renderUpload(c.files).appendTo(a(this).find(".files")).fadeIn(function () {
                    a(this).show()
                }).data("data", c);
                if ((d.options.autoUpload || c.autoUpload) && c.isValidated) {
                    c.jqXHR = c.submit()
                }
            },
            send: function (b, c) {
                if (!c.isValidated) {
                    var d = a(this).data("fileupload");
                    if (!c.isAdjusted) {
                        d._adjustMaxNumberOfFiles(-c.files.length)
                    }
                    if (!d._validate(c.files)) {
                        return false
                    }
                }
                if (c.context && c.dataType && c.dataType.substr(0, 6) === "iframe") {
                    c.context.find(".ui-progressbar").progressbar("value", parseInt(100, 10))
                }
            },
            done: function (b, c) {
                var d = a(this).data("fileupload");
                if (c.context) {
                    c.context.each(function (b) {
                        var e = a.isArray(c.result) && c.result[b] || {
                            error: "emptyResult"
                        };
                        if (e.error) {
                            d._adjustMaxNumberOfFiles(1)
                        }
                        a(this).fadeOut(function () {
                            d._renderDownload([e]).css("display", "none").replaceAll(this).fadeIn(function () {
                                a(this).show()
                            })
                        })
                    })
                } else {
                    d._renderDownload(c.result).css("display", "none").appendTo(a(this).find(".files")).fadeIn(function () {
                        a(this).show()
                    })
                }
            },
            fail: function (b, c) {
                var d = a(this).data("fileupload");
                d._adjustMaxNumberOfFiles(c.files.length);
                if (c.context) {
                    c.context.each(function (b) {
                        a(this).fadeOut(function () {
                            if (c.errorThrown !== "abort") {
                                var e = c.files[b];
                                e.error = e.error || c.errorThrown || true;
                                d._renderDownload([e]).css("display", "none").replaceAll(this).fadeIn(function () {
                                    a(this).show()
                                })
                            } else {
                                c.context.remove()
                            }
                        })
                    })
                } else if (c.errorThrown !== "abort") {
                    d._adjustMaxNumberOfFiles(-c.files.length);
                    c.context = d._renderUpload(c.files).css("display", "none").appendTo(a(this).find(".files")).fadeIn(function () {
                        a(this).show()
                    }).data("data", c)
                }
            },
            progress: function (a, b) {
                if (b.context) {
                    b.context.find(".ui-progressbar").progressbar("value", parseInt(b.loaded / b.total * 100, 10))
                }
            },
            destroy: function (b, c) {
                var d = a(this).data("fileupload");
                if (c.url) {
                    a.ajax(c).success(function () {
                        d._adjustMaxNumberOfFiles(1);
                        a(this).fadeOut(function () {
                            a(this).remove()
                        })
                    })
                } else {
                    c.context.fadeOut(function () {
                        a(this).remove()
                    })
                }
            }
        },
        // Scales the given image (img HTML element)
        // using the given options.
        // Returns a canvas object if the canvas option is true
        // and the browser supports canvas, else the scaled image:
        _scaleImage: function (img, options) {
            options = options || {};
            var canvas = document.createElement('canvas'),
                scale = Math.min(
                (options.maxWidth || img.width) / img.width, (options.maxHeight || img.height) / img.height);
            if (scale >= 1) {
                scale = Math.max(
                (options.minWidth || img.width) / img.width, (options.minHeight || img.height) / img.height);
            }
            img.width = parseInt(img.width * scale, 10);
            img.height = parseInt(img.height * scale, 10);
            if (!options.canvas || !canvas.getContext) {
                return img;
            }
            canvas.width = img.width;
            canvas.height = img.height;
            canvas.getContext('2d').drawImage(img, 0, 0, img.width, img.height);
            return canvas;
        },

        _createObjectURL: function (file) {
            var undef = 'undefined',
                urlAPI = (typeof window.createObjectURL !== undef && window) || (typeof URL !== undef && URL) || (typeof webkitURL !== undef && webkitURL);
            return urlAPI ? urlAPI.createObjectURL(file) : false;
        },

        _revokeObjectURL: function (url) {
            var undef = 'undefined',
                urlAPI = (typeof window.revokeObjectURL !== undef && window) || (typeof URL !== undef && URL) || (typeof webkitURL !== undef && webkitURL);
            return urlAPI ? urlAPI.revokeObjectURL(url) : false;
        },

        // Loads a given File object via FileReader interface,
        // invokes the callback with a data url:
        _loadFile: function (file, callback) {
            if (typeof FileReader !== 'undefined' && FileReader.prototype.readAsDataURL) {
                var fileReader = new FileReader();
                fileReader.onload = function (e) {
                    callback(e.target.result);
                };
                fileReader.readAsDataURL(file);
                return true;
            }
            return false;
        },

        // Loads an image for a given File object.
        // Invokes the callback with an img or optional canvas
        // element (if supported by the browser) as parameter:
        _loadImage: function (file, callback, options) {
            var that = this,
                url, img;
            if (!options || !options.fileTypes || options.fileTypes.test(file.type)) {
                url = this._createObjectURL(file);
                img = $('<img>').bind('load', function () {
                    $(this).unbind('load');
                    that._revokeObjectURL(url);
                    callback(that._scaleImage(img[0], options));
                }).prop('src', url);
                if (!url) {
                    this._loadFile(file, function (url) {
                        img.prop('src', url);
                    });
                }
            }
        },

        _enableDragToDesktop: function () {
            var b = a(this),
                c = b.prop("href"),
                d = decodeURIComponent(c.split("/").pop()).replace(/:/g, "-"),
                e = "application/octet-stream";
            b.bind("dragstart", function (a) {
                try {
                    a.originalEvent.dataTransfer.setData("DownloadURL", [e, d, c].join(":"))
                } catch (b) {}
            })
        },
        _adjustMaxNumberOfFiles: function (a) {
            if (typeof this.options.maxNumberOfFiles === "number") {
                this.options.maxNumberOfFiles += a;
                if (this.options.maxNumberOfFiles < 1) {
                    this._disableFileInputButton()
                } else {
                    this._enableFileInputButton()
                }
            }
        },
        _maxNumberOfFilesReached: function (a) {
            if (typeof this.options.maxNumberOfFiles === "number") {
                var b = this.options.maxNumberOfFiles + a;
                if (b < 1) {
                    return true
                } else {
                    return false
                }
            }
        },
        _formatFileSize: function (a) {
            if (typeof a.size !== "number") {
                return ""
            }
            if (a.size >= 1e9) {
                return (a.size / 1e9).toFixed(2) + " GB"
            }
            if (a.size >= 1e6) {
                return (a.size / 1e6).toFixed(2) + " MB"
            }
            return (a.size / 1e3).toFixed(2) + " KB"
        },
        _hasError: function (a) {
            if (a.error) {
                return a.error
            }
            if (this.options.maxNumberOfFiles < 0) {
                return "maxNumberOfFiles"
            }
            if (!(this.options.acceptFileTypes.test(a.type) || this.options.acceptFileTypes.test(a.name))) {
                return "acceptFileTypes"
            }
            if (this.options.maxFileSize && a.size > this.options.maxFileSize) {
                return "maxFileSize"
            }
            if (typeof a.size === "number" && a.size < this.options.minFileSize) {
                return "minFileSize"
            }
            return null
        },
        _validate: function (b) {
            var c = this,
                d;
            a.each(b, function (a, b) {
                b.error = c._hasError(b);
                d = !b.error
            });
            return d
        },
        _uploadTemplateHelper: function (a) {
            a.sizef = this._formatFileSize(a);
            return a
        },
        _renderUploadTemplate: function (b) {
            var c = this;
            return a.tmpl(this.options.uploadTemplate, a.map(b, function (a) {
                return c._uploadTemplateHelper(a)
            }))
        },
        _renderUpload: function (b) {
            var c = this,
                d = this.options,
                e = this._renderUploadTemplate(b);
            if (!(e instanceof a)) {
                return a()
            }
            e.css("display", "none");
            e.find(".progress div").slice(1).remove().end().first().progressbar();
            e.find(".cancel a").slice(1).remove().end().first().button({
                text: false,
                icons: {
                    primary: "ui-icon-cancel"
                }
            });
            if (d.previewRequired) {
                e.find('.preview').each(function (index, node) {
                    c._loadImage(
                    b[index], function (img) {
                        $(img).hide().appendTo(node).fadeIn();
                    }, {
                        maxWidth: d.previewMaxWidth,
                        maxHeight: d.previewMaxHeight,
                        fileTypes: d.previewFileTypes,
                        canvas: d.previewAsCanvas
                    });
                });
            }
            return e
        },
        _downloadTemplateHelper: function (a) {
            a.sizef = this._formatFileSize(a);
            return a
        },
        _renderDownloadTemplate: function (b) {
            var c = this;
            return a.tmpl(this.options.downloadTemplate, a.map(b, function (a) {
                return c._downloadTemplateHelper(a)
            }))
        },
        _renderDownload: function (b) {
            var c = this._renderDownloadTemplate(b);
            if (!(c instanceof a)) {
                return a()
            }
            c.css("display", "none");
            c.find("a").each(this._enableDragToDesktop);
            return c
        },
        _startHandler: function (b) {
            b.preventDefault();
            var c = a(this).closest(".template-upload"),
                d = c.data("data");
            if (d && d.submit && !d.jqXHR) {
                d.jqXHR = d.submit();
                a(this).fadeOut()
            }
        },
        _cancelHandler: function (b) {
            b.preventDefault();
            var c = a(this).closest(".template-upload"),
                d = c.data("data") || {};
            if (!d.jqXHR) {
                d.errorThrown = "abort";
                b.data.fileupload._trigger("fail", b, d)
            } else {
                d.jqXHR.abort()
            }
        },
        _deleteHandler: function (b) {
            b.preventDefault();
            var c = a(this);
            b.data.fileupload._trigger("destroy", b, {
                context: c.closest(".template-download"),
                url: c.attr("data-url"),
                type: c.attr("data-type"),
                dataType: b.data.fileupload.options.dataType
            })
        },
        _initEventHandlers: function () {
            a.blueimp.fileupload.prototype._initEventHandlers.call(this);
            var b = this.element.find(".files"),
                c = {
                    fileupload: this
                };
            b.find('.start').live('click.' + this.options.namespace,c,this._startHandler);
            b.find(".cancel a").live("click." + this.options.namespace, c, this._cancelHandler);
            b.find(".delete a").live("click." + this.options.namespace, c, this._deleteHandler)
        },
        _destroyEventHandlers: function () {
            var b = this.element.find(".files");
            b.find(".cancel a").die("click." + this.options.namespace);
            b.find(".delete a").die("click." + this.options.namespace);
            a.blueimp.fileupload.prototype._destroyEventHandlers.call(this)
        },
        _initFileUploadButtonBar: function () {
            var b = this.element.find(".fileupload-buttonbar"),
                c = this.element.find(".files"),
                d = this.options.namespace;
            this.element.find(".fileinput-button").each(function () {
                var b = a(this).find("input:file").detach();
                a(this).button({
                    icons: {
                        primary: "ui-icon-plusthick"
                    }
                }).append(b)
            });
            b.find(".cancel").button({
                icons: {
                    primary: "ui-icon-cancel"
                }
            }).bind("click." + d, function (a) {
                a.preventDefault();
                c.find(".cancel a").click()
            });
            b.find(".delete").bind("click." + d, function (a) {
                a.preventDefault();
                c.find(".delete a").click()
            })
        },
        _destroyFileUploadButtonBar: function () {
            this.element.find(".fileinput-button").each(function () {
                var b = a(this).find("input:file").detach();
                a(this).button("destroy").append(b)
            });
            this.element.find(".fileupload-buttonbar button").unbind("click." + this.options.namespace).button("destroy")
        },
        _enableFileInputButton: function () {
            this.element.find(".fileinput-button input:file:disabled").each(function () {
                var b = a(this),
                    c = b.parent();
                b.detach().prop("disabled", false);
                c.button("enable").append(b)
            })
        },
        _disableFileInputButton: function () {
            this.element.find(".fileinput-button input:file:enabled").each(function () {
                var b = a(this),
                    c = b.parent();
                b.detach().prop("disabled", true);
                c.button("disable").append(b)
            })
        },
        _initTemplates: function () {
            if (this.options.uploadTemplate instanceof a && !this.options.uploadTemplate.length) {
                this.options.uploadTemplate = a(this.options.uploadTemplate.selector)
            }
            if (this.options.downloadTemplate instanceof a && !this.options.downloadTemplate.length) {
                this.options.downloadTemplate = a(this.options.downloadTemplate.selector)
            }
        },
        _create: function () {
            a.blueimp.fileupload.prototype._create.call(this);
            this._initTemplates();
            this._initFileUploadButtonBar()
        },
        destroy: function () {
            this._destroyFileUploadButtonBar();
            a.blueimp.fileupload.prototype.destroy.call(this)
        },
        enable: function () {
            a.blueimp.fileupload.prototype.enable.call(this);
            this.element.find(":ui-button").not(".fileinput-button").button("enable");
            this._enableFileInputButton()
        },
        disable: function () {
            this.element.find(":ui-button").not(".fileinput-button").button("disable");
            this._disableFileInputButton();
            a.blueimp.fileupload.prototype.disable.call(this)
        }
    })
})(jQuery);
(function (a) {
    "use strict";
    var b = 0;
    a.ajaxTransport("iframe", function (c, d, e) {
        if (c.type === "POST" || c.type === "GET") {
            var f, g;
            return {
                send: function (d, e) {
                    f = a('<form style="display:none;"></form>');
                    g = a('<iframe src="javascript:false;" name="iframe-transport-' + (b += 1) + '"></iframe>').bind("load", function () {
                        var b;
                        g.unbind("load").bind("load", function () {
                            var b;
                            try {
                                b = g.contents();
                                if (!b.length || !b[0].firstChild) {
                                    throw new Error
                                }
                            } catch (c) {
                                b = undefined
                            }
                            e(200, "success", {
                                iframe: b
                            });
                            a('<iframe src="javascript:false;"></iframe>').appendTo(f);
                            f.remove()
                        });
                        f.prop("target", g.prop("name")).prop("action", c.url).prop("method", c.type);
                        if (c.formData) {
                            a.each(c.formData, function (b, c) {
                                var hiddenval=a('<input type="hidden"/>').attr("name", c.name);
								if(hiddenval && hiddenval!=undefined){hiddenval.val(c.value).appendTo(f);}
                            })
                        }
                        if (c.fileInput && c.fileInput.length && c.type === "POST") {
                            b = c.fileInput.clone();
                            c.fileInput.after(function (a) {
                                return b[a]
                            });
                            if (c.paramName) {
                                c.fileInput.each(function () {
                                    a(this).prop("name", c.paramName)
                                })
                            }
                            f.append(c.fileInput).prop("enctype", "multipart/form-data").prop("encoding", "multipart/form-data")
                        }
                        f.submit();
                        if (b && b.length) {
                            c.fileInput.each(function (c, d) {
                                var e = a(b[c]);
                                a(d).prop("name", e.prop("name"));
                                e.replaceWith(d)
                            })
                        }
                    });
                    f.append(g).appendTo("body")
                },
                abort: function () {
                    if (g) {
                        g.unbind("load").prop("src", "javascript".concat(":false;"))
                    }
                    if (f) {
                        f.remove()
                    }
                }
            }
        }
    });
    a.ajaxSetup({
        converters: {
            "iframe text": function (a) {
                return a.text()
            },
            "iframe json": function (b) {
                return a.parseJSON(b.text())
            },
            "iframe html": function (a) {
                return a.find("body").html()
            },
            "iframe script": function (b) {
                return a.globalEval(b.text())
            }
        }
    })
})(jQuery);
(function (a) {
    function x() {
        var b = this.nodes;
        a.tmpl(null, null, null, this).insertBefore(b[0]);
        a(b).remove()
    }

    function w(b, c) {
        var d = this._wrap;
        return a.map(a(a.isArray(d) ? d.join("") : d).filter(b || "*"), function (a) {
            return c ? a.innerText || a.textContent : a.outerHTML || r(a)
        })
    }

    function v(b, c) {
        var d = b.options || {};
        d.wrapped = c;
        return a.tmpl(a.template(b.tmpl), b.data, d, b.item)
    }

    function u(b, c, d) {
        return a.tmpl(a.template(b), c, d, this)
    }

    function t(a, b, c, d) {
        if (!a) return k.pop();
        k.push({
            _: a,
            tmpl: b,
            item: this,
            data: c,
            options: d
        })
    }

    function s(b) {
        function p(b) {
            function p(a) {
                a = a + d;
                n = k[a] = k[a] || l(n, e[n.parent.key + d] || n.parent, null, true)
            }
            var g, h = b,
                m, n, o;
            if (o = b.getAttribute(c)) {
                while (h.parentNode && (h = h.parentNode).nodeType === 1 && !(g = h.getAttribute(c)));
                if (g !== o) {
                    h = h.parentNode ? h.nodeType === 11 ? 0 : h.getAttribute(c) || 0 : 0;
                    if (!(n = e[o])) {
                        n = f[o];
                        n = l(n, e[h] || f[h], null, true);
                        n.key = ++i;
                        e[i] = n
                    }
                    j && p(o)
                }
                b.removeAttribute(c)
            } else if (j && (n = a.data(b, "tmplItem"))) {
                p(n.key);
                e[n.key] = n;
                h = a.data(b.parentNode, "tmplItem");
                h = h ? h.key : 0
            }
            if (n) {
                m = n;
                while (m && m.key != h) {
                    m.nodes.push(b);
                    m = m.parent
                }
                delete n._ctnt;
                delete n._wrap;
                a.data(b, "tmplItem", n)
            }
        }
        var d = "_" + j,
            g, h, k = {},
            m, n, o;
        for (m = 0, n = b.length; m < n; m++) {
            if ((g = b[m]).nodeType !== 1) continue;
            h = g.getElementsByTagName("*");
            for (o = h.length - 1; o >= 0; o--) p(h[o]);
            p(g)
        }
    }

    function r(a) {
        var b = document.createElement("div");
        b.appendChild(a.cloneNode(true));
        return b.innerHTML
    }

    function q(a) {
        return a ? a.replace(/\\'/g, "'").replace(/\\\\/g, "\\") : null
    }

    function p(b, c) {
        b._wrap = m(b, true, a.isArray(c) ? c : [d.test(c) ? c : a(c).html()]).join("")
    }

    function o(b) {
        return new Function("jQuery", "$item", "var $=jQuery,call,_=[],$data=$item.data;with($data){_.push('" + a.trim(b).replace(/([\\'])/g, "\\$1").replace(/[\r\t\n]/g, " ").replace(/\$\{([^\}]*)\}/g, "{{= $1}}").replace(/\{\{(\/?)(\w+|.)(?:\(((?:[^\}]|\}(?!\}))*?)?\))?(?:\s+(.*?)?)?(\(((?:[^\}]|\}(?!\}))*?)\))?\s*\}\}/g, function (b, c, d, e, f, g, h) {
            var i = a.tmpl.tag[d],
                j, k, l;
            if (!i) throw "Template command not found: " + d;
            j = i._default || [];
            if (g && !/\w$/.test(f)) {
                f += g;
                g = ""
            }
            if (f) {
                f = q(f);
                h = h ? "," + q(h) + ")" : g ? ")" : "";
                k = g ? f.indexOf(".") > -1 ? f + g : "(" + f + ").call($item" + h : f;
                l = g ? k : "(typeof(" + f + ")==='function'?(" + f + ").call($item):(" + f + "))"
            } else l = k = j.$1 || "null";
            e = q(e);
            return "');" + i[c ? "close" : "open"].split("$notnull_1").join(f ? "typeof(" + f + ")!=='undefined' && (" + f + ")!=null" : "true").split("$1a").join(l).split("$1").join(k).split("$2").join(e ? e.replace(/\s*([^\(]+)\s*(\((.*?)\))?/g, function (a, b, c, d) {
                d = d ? "," + d + ")" : c ? ")" : "";
                return d ? "(" + b + ").call($item" + d : a
            }) : j.$2 || "") + "_.push('"
        }) + "');}return _;")
    }

    function n(b) {
        var c = document.createElement("div");
        c.innerHTML = b;
        return a.makeArray(c.childNodes)
    }

    function m(b, d, e) {
        var f, g = e ? a.map(e, function (a) {
            return typeof a === "string" ? b.key ? a.replace(/(<\w+)(?=[\s>])(?![^>]*_tmplitem)([^>]*)/g, "$1 " + c + '="' + b.key + '" $2') : a : m(a, b, a._ctnt)
        }) : b;
        if (d) return g;
        g = g.join("");
        g.replace(/^\s*([^<\s][^<]*)?(<[\w\W]+>)([^>]*[^>\s])?\s*$/, function (b, c, d, e) {
            f = a(d).get();
            s(f);
            if (c) f = n(c).concat(f);
            if (e) f = f.concat(n(e))
        });
        return f ? f : n(g)
    }

    function l(b, c, d, g) {
        var h = {
            data: g || (c ? c.data : {}),
            _wrap: c ? c._wrap : null,
            tmpl: null,
            parent: c || null,
            nodes: [],
            calls: t,
            nest: u,
            wrap: v,
            html: w,
            update: x
        };
        b && a.extend(h, b, {
            nodes: [],
            parent: c
        });
        if (d) {
            h.tmpl = d;
            h._ctnt = h._ctnt || h.tmpl(a, h);
            h.key = ++i;
            (k.length ? f : e)[i] = h
        }
        return h
    }
    var b = a.fn.domManip,
        c = "_tmplitem",
        d = /^[^<]*(<[\w\W]+>)[^>]*$|\{\{\! /,
        e = {},
        f = {},
        g, h = {
            key: 0,
            data: {}
        },
        i = 0,
        j = 0,
        k = [];
    a.each({
        appendTo: "append",
        prependTo: "prepend",
        insertBefore: "before",
        insertAfter: "after",
        replaceAll: "replaceWith"
    }, function (b, c) {
        a.fn[b] = function (d) {
            var f = [],
                h = a(d),
                i, k, l, m, n = this.length === 1 && this[0].parentNode;
            g = e || {};
            if (n && n.nodeType === 11 && n.childNodes.length === 1 && h.length === 1) {
                h[c](this[0]);
                f = this
            } else {
                for (k = 0, l = h.length; k < l; k++) {
                    j = k;
                    i = (k > 0 ? this.clone(true) : this).get();
                    a.fn[c].apply(a(h[k]), i);
                    f = f.concat(i)
                }
                j = 0;
                f = this.pushStack(f, b, h.selector)
            }
            m = g;
            g = null;
            a.tmpl.complete(m);
            return f
        }
    });
    a.fn.extend({
        tmpl: function (b, c, d) {
            return a.tmpl(this[0], b, c, d)
        },
        tmplItem: function () {
            return a.tmplItem(this[0])
        },
        template: function (b) {
            return a.template(b, this[0])
        },
        domManip: function (c, d, f) {
            if (c[0] && c[0].nodeType) {
                var h = a.makeArray(arguments),
                    i = c.length,
                    k = 0,
                    l;
                while (k < i && !(l = a.data(c[k++], "tmplItem")));
                if (i > 1) h[0] = [a.makeArray(c)];
                if (l && j) h[2] = function (b) {
                    a.tmpl.afterManip(this, b, f)
                };
                b.apply(this, h)
            } else b.apply(this, arguments);
            j = 0;
            !g && a.tmpl.complete(e);
            return this
        }
    });
    a.extend({
        tmpl: function (b, c, d, g) {
            var i, j = !g;
            if (j) {
                g = h;
                b = a.template[b] || a.template(null, b);
                f = {}
            } else if (!b) {
                b = g.tmpl;
                e[g.key] = g;
                g.nodes = [];
                g.wrapped && p(g, g.wrapped);
                return a(m(g, null, g.tmpl(a, g)))
            }
            if (!b) return [];
            if (typeof c === "function") c = c.call(g || {});
            d && d.wrapped && p(d, d.wrapped);
            i = a.isArray(c) ? a.map(c, function (a) {
                return a ? l(d, g, b, a) : null
            }) : [l(d, g, b, c)];
            return j ? a(m(g, null, i)) : i
        },
        tmplItem: function (b) {
            var c;
            if (b instanceof a) b = b[0];
            while (b && b.nodeType === 1 && !(c = a.data(b, "tmplItem")) && (b = b.parentNode));
            return c || h
        },
        template: function (b, c) {
            if (c) {
                if (typeof c === "string") c = o(c);
                else if (c instanceof a) c = c[0] || {};
                if (c.nodeType) c = a.data(c, "tmpl") || a.data(c, "tmpl", o(c.innerHTML));
                return typeof b === "string" ? a.template[b] = c : c
            }
            return b ? typeof b !== "string" ? a.template(null, b) : a.template[b] || a.template(null, d.test(b) ? b : a(b)) : null
        },
        encode: function (a) {
            return ("" + a).split("<").join("<").split(">").join(">").split('"').join("&#34;").split("'").join("&#39;")
        }
    });
    a.extend(a.tmpl, {
        tag: {
            tmpl: {
                _default: {
                    $2: "null"
                },
                open: "if($notnull_1){_=_.concat($item.nest($1,$2));}"
            },
            wrap: {
                _default: {
                    $2: "null"
                },
                open: "$item.calls(_,$1,$2);_=[];",
                close: "call=$item.calls();_=call._.concat($item.wrap(call,_));"
            },
            each: {
                _default: {
                    $2: "$index, $value"
                },
                open: "if($notnull_1){$.each($1a,function($2){with(this){",
                close: "}});}"
            },
            "if": {
                open: "if(($notnull_1) && $1a){",
                close: "}"
            },
            "else": {
                _default: {
                    $1: "true"
                },
                open: "}else if(($notnull_1) && $1a){"
            },
            html: {
                open: "if($notnull_1){_.push($1a);}"
            },
            "=": {
                _default: {
                    $1: "$data"
                },
                open: "if($notnull_1){_.push($.encode($1a));}"
            },
            "!": {
                open: ""
            }
        },
        complete: function () {
            e = {}
        },
        afterManip: function (b, c, d) {
            var e = c.nodeType === 11 ? a.makeArray(c.childNodes) : c.nodeType === 1 ? [c] : [];
            d.call(b, c);
            s(e);
            j++
        }
    })
})(jQuery)