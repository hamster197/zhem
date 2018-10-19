(function () {
	$(document).ready(function() {
		$("#{{ input_id }}").datetimepicker({{ options|safe }});
	});
})(jQuery);