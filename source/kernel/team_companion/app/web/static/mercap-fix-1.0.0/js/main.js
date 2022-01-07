//Fix Map for Internet Explorer 8 - Begin
//https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map?redirectlocale=en-US&redirectslug=JavaScript%2FReference%2FGlobal_Objects%2FArray%2Fmap
//------------------------------------------------------------
// Test enhancement proposition
// When testing for new native methods, like Array.prototype.map,
// maybe an extensive test should replace the simple if (!Arrray.prototype.map).
// Maybe include [native code] string existence test?

// console.log(Array.prototype.map.toString());
// > function map() {
// >   [native code]
// > }

// Otherwise
// Array.prototype.map = "map";
// tests true but not for behavior

// Production steps of ECMA-262, Edition 5, 15.4.4.19
// Reference: http://es5.github.com/#x15.4.4.19
if (!Array.prototype.map) {
  Array.prototype.map = function(callback, thisArg) {

     var T, A, k;

     if (this == null) {
        throw new TypeError(" this is null or not defined");
     }

     // 1. Let O be the result of calling ToObject passing the |this| value as the argument.
     var O = Object(this);

     // 2. Let lenValue be the result of calling the Get internal method of O with the argument "length".
     // 3. Let len be ToUint32(lenValue).
     var len = O.length >>> 0;

     // 4. If IsCallable(callback) is false, throw a TypeError exception.
     // See: http://es5.github.com/#x9.11
     if (typeof callback !== "function") {
        throw new TypeError(callback + " is not a function");
     }

     // 5. If thisArg was supplied, let T be thisArg; else let T be undefined.
     if (thisArg) {
        T = thisArg;
     }

     // 6. Let A be a new array created as if by the expression new Array(len) where Array is
     // the standard built-in constructor with that name and len is the value of len.
     A = new Array(len);

     // 7. Let k be 0
     k = 0;

     // 8. Repeat, while k < len
     while(k < len) {

        var kValue, mappedValue;

        // a. Let Pk be ToString(k).
        //   This is implicit for LHS operands of the in operator
        // b. Let kPresent be the result of calling the HasProperty internal method of O with argument Pk.
        //   This step can be combined with c
        // c. If kPresent is true, then
        if (k in O) {

          // i. Let kValue be the result of calling the Get internal method of O with argument Pk.
          kValue = O[ k ];

          // ii. Let mappedValue be the result of calling the Call internal method of callback
          // with T as the this value and argument list containing kValue, k, and O.
          mappedValue = callback.call(T, kValue, k, O);

          // iii. Call the DefineOwnProperty internal method of A with arguments
          // Pk, Property Descriptor {Value: mappedValue, : true, Enumerable: true, Configurable: true},
          // and false.

          // In browsers that support Object.defineProperty, use the following:
          // Object.defineProperty(A, Pk, { value: mappedValue, writable: true, enumerable: true, configurable: true });

          // For best browser support, use the following:
          A[ k ] = mappedValue;
        }
        // d. Increase k by 1.
        k++;
     }

     // 9. return A
     return A;
  };      
}
//Fix Map for Internet Explorer 8 - End
//------------------------------------------------------------
//Fix IndexOf for Internet Explorer 8 - Begin
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf
// Production steps of ECMA-262, Edition 5, 15.4.4.14
// Reference: http://es5.github.io/#x15.4.4.14
if (!Array.prototype.indexOf) {
  Array.prototype.indexOf = function(searchElement, fromIndex) {

    var k;

    // 1. Let O be the result of calling ToObject passing
    //    the this value as the argument.
    if (this == null) {
      throw new TypeError('"this" is null or not defined');
    }

    var O = Object(this);

    // 2. Let lenValue be the result of calling the Get
    //    internal method of O with the argument "length".
    // 3. Let len be ToUint32(lenValue).
    var len = O.length >>> 0;

    // 4. If len is 0, return -1.
    if (len === 0) {
      return -1;
    }

    // 5. If argument fromIndex was passed let n be
    //    ToInteger(fromIndex); else let n be 0.
    var n = +fromIndex || 0;

    if (Math.abs(n) === Infinity) {
      n = 0;
    }

    // 6. If n >= len, return -1.
    if (n >= len) {
      return -1;
    }

    // 7. If n >= 0, then Let k be n.
    // 8. Else, n<0, Let k be len - abs(n).
    //    If k is less than 0, then let k be 0.
    k = Math.max(n >= 0 ? n : len - Math.abs(n), 0);

    // 9. Repeat, while k < len
    while (k < len) {
      // a. Let Pk be ToString(k).
      //   This is implicit for LHS operands of the in operator
      // b. Let kPresent be the result of calling the
      //    HasProperty internal method of O with argument Pk.
      //   This step can be combined with c
      // c. If kPresent is true, then
      //    i.  Let elementK be the result of calling the Get
      //        internal method of O with the argument ToString(k).
      //   ii.  Let same be the result of applying the
      //        Strict Equality Comparison Algorithm to
      //        searchElement and elementK.
      //  iii.  If same is true, return k.
      if (k in O && O[k] === searchElement) {
        return k;
      }
      k++;
    }
    return -1;
  };
}
//Fix IndexOf for Internet Explorer 8 - End
function updateTreeSelection(node, hiddenMultipleSelectionID)
{
    var selectedNodes = node.tree.getSelectedNodes();
    var selectedDescriptions = $.map(selectedNodes, function(node){
        return node.data.title;
    });
    $("#" + hiddenMultipleSelectionID + " option").each(function() {
        var adaptedOption = $(this);
        adaptedOption.prop("selected", (selectedDescriptions.indexOf(adaptedOption.text()) > -1));
    });
};

/*Quiz�s esto se usa en reportes*/
function callHidden (a) {
    console.log(a);
    $("input[name='view']").val(a).trigger("change");
};

function functionCleanModals(aContainerClass,aModal,anExpectedClass){
    //Conditional execution to avoid problems in IE8 (aModal does not understand remove)
    if (typeof aModal.remove != "undefined") { 
        aModal.remove();
    }
    
    var scriptsRemaining = $("."+aContainerClass).children("script");
    var leftoversRemaining = $("."+aContainerClass).children("."+anExpectedClass);
    if ((scriptsRemaining.size()+leftoversRemaining.size())===$("."+aContainerClass).children().size()) {
        scriptsRemaining.remove();
        leftoversRemaining.remove();
        $("div.modal-backdrop").remove();
    }}
function functionCleanPopovers(aCssClass){
    $("."+aCssClass).popover("hide");}
function functionRedirect(url){
    var form = $('<form action="' + url + '" method="post">' +
        '<input type="text" name="redirect" value="true" />' +
        '</form>');
    $('body').append(form);
    form.submit();
}
function functionWidgetDistribution(columnCssClass,titleAttribute){var positions = new Array();
  var titleAttributeName = "data-" + titleAttribute;
  $("." + columnCssClass).each(function(zeroBasedColumnIndex) {
    var columnPositions = new Array();
    $(this).find($("[" + titleAttributeName + "]")).each(function(zeroBasedPanelIndex) {
      var title = this.getAttribute(titleAttributeName);
      var visible = $(this).has("."+"in").size() > 0;
      columnPositions.push({"title": title, "visible": visible});
    })
    positions.push(columnPositions);
  });
  return positions}

!function ($) {

  "use strict"; // jshint ;_;

/* DYNATREE API */
    if($.ui.dynatree){
    //Prevent Dynatree from using folder icons
    $.ui.dynatree.nodedatadefaults["icon"] = false;
    };

/* HIGHCHARTS API */
    if($.Highcharts){
    Highcharts.Renderer.prototype.symbols.line = function (x, y, width, height) {
        return ["M", x, y+height/2, "L", x + height, y+height/2];
    }};

}(window.jQuery);
(function(){Willow.handleAjaxErrorCall=function(theXMLHttpRequest,textStatus,errorThrown){if(theXMLHttpRequest.getAllResponseHeaders()){if(theXMLHttpRequest["status"]=="500"){$(".willow-dialog-container").first().append("<div class=\"modal\" tabindex=\"-1\" role=\"dialog\"><div class=\"modal-dialog modal-lg unexpected-error\" role=\"document\"><div class=\"modal-content\"><div class=\"modal-header\"><button class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\" type=\"button\"><span aria-hidden=\"true\">x</span></button><h4 class=\"modal-title\">Error inesperado</h4></div><div class=\"modal-body\"><div><p>Se produjo un error inesperado. Por favor comun�quelo a soporte t�cnico</p></div><fieldset><legend>Informaci�n T�cnica</legend><span class=\"unexpected-error-place-holder\"></span></fieldset></div><div class=\"modal-footer\"><button class=\"btn\" data-dismiss=\"modal\" type=\"button\">Close</button></div></div></div></div>");$(".unexpected-error-place-holder").text(theXMLHttpRequest["responseText"])} else {if(theXMLHttpRequest["status"]=="403"){$(".willow-dialog-container").first().append("<div class=\"modal unexpected-error\" tabindex=\"-1\" role=\"dialog\" id=\"id1\"><div class=\"modal-dialog modal-lg\" role=\"document\"><div class=\"modal-content\"><div class=\"modal-header\"><button id=\"button-id2\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\" type=\"button\"><span aria-hidden=\"true\">x</span></button><h4 class=\"modal-title\">Sesi�n terminada por inactividad</h4></div><div class=\"modal-body\"><div><p>Su sesi�n ya no est� activa. Se super� el tiempo m�ximo de inactividad.</p></div></div><div class=\"modal-footer\"><button id=\"button-id3\" class=\"btn btn-link\" data-dismiss=\"modal\" type=\"button\">Cerrar</button></div></div></div></div><script type=\"text/javascript\">$(\"#id1\").modal({\"backdrop\":\"static\"}).on(\"hidden.bs.modal\",function(){Willow.Bootstrap.cleanModal($(this))});$(\"#button-id2\").click(function(event){window.location.replace(window.location.pathname)});$(\"#button-id3\").click(function(event){window.location.replace(window.location.pathname)});</script>")} else {alert("No se pudo completar el pedido en el servidor. Por favor revise su conexi�n y vuelva a intentarlo.\n\nInformaci�n adicional\nStatus: " + theXMLHttpRequest["status"] +"\nError Thrown: " + errorThrown +"\nText Status: "+ textStatus + "\n\nResponse: "+ theXMLHttpRequest["responseText"] + "")}}}}}());
//---------------------------
//This function inserts into "textField" the text "newText" at the cursor position
function insertAtCursor(textField, newText) {
    "use strict";
    var start = textField.prop("selectionStart"),
        end = textField.prop("selectionEnd"),
        text = textField.val(),
        before = text.substring(0, start),
        after = text.substring(end, text.length);
    textField.val(before + newText + after);
    textField[0].selectionStart = textField[0].selectionEnd = start + newText.length;
    textField.focus();
};