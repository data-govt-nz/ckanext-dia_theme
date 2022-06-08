'use strict';

(function ($) {
  var showBanner = function (content) {
    if (content) {
      $('header').after(content)
    }
  }

  var getBannerHost = function () {
    var local = window.location.host.startsWith('ckan-gateway')
    if (local) {
      return 'http://ckan-gateway:8000'
    }

    var production = window.location.host.startsWith('catalogue')
    return production ? '//data.govt.nz' : '//diadata-uat.cwp.govt.nz'
  }

  var getBanner = function () {
    $.ajax({
      url: getBannerHost() + '/api/banner',
      success: function (banner) {
        if (banner.enabled) {
          showBanner(banner.content)
        }
      }
    })
  }

  getBanner();
})($)
