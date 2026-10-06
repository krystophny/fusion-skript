/**
 * Copyright (C) 2013 STATISTIK AUSTRIA
 */
if (!jQuery) { throw new Error("This script requires jQuery") }

+function ($) { "use strict";

  $(document).on('click.bs.collapse.data-api', '[data-toggle=collapse]', function (e) {
	if (this.href) window.location.href = this.href;
	self.scrollTo(0, 0);
  })

  $(window).on('load', function () {
	var param = window.location.href.split('#')[1]
	if (param) {
	  var obj = $('a[href=#'+param+']')
	  if (obj) obj.trigger('click.bs.collapse.data-api')
	}
  })

}(window.jQuery);
