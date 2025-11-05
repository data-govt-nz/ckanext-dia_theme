'use strict';

(function ($) {
  var showBanner = function (content) {
    if (content) {
      $('header.site-header').after(content)
    }
  }

  var getBannerHost = function () {
    var local = window.location.host.startsWith('ckan-gateway')
    if (local) {
      return 'http://localhost:8000'
    }

    var production = window.location.host.startsWith('catalogue')
    return production ? '//data.govt.nz' : '//diadata2-uat.sites.silverstripe.com'
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
