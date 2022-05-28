require(['jquery', 'music21'], function() {
    var common = music21.common;
    
    feedback = {};
    feedback.alertTypes = {
            'alert': { // something bad happened
                'background-color': 'red',
                color: 'white',
                'font-weight': 'bold',
                delayFade: 10 * 1000,
            },
            'ok': { // fine -- all good. green
                'background-color': '#99ff99',
                delayFade: 10 * 1000,
                fadeTime: 2 * 1000,            
            },
            'update': {  // neutral -- could be a bit good or neutral
                'background-color': '#e4f0f0',
                delayFade: 4 * 1000,
            },
            'normal': { }, // default -- yellow, alert
    };
        
    feedback.alert = function (msg, type, params) {
        type = type || 'normal';
                        
        cssParams = {
                top: '80px',
                'background-color': '#ffff99',
                color: 'black',
                'font-weight': 'normal',
                'position': 'fixed',
                'left': '750px',
                'width': '200px',
                'opacity': .9,
                'border-radius': '15px',
                'box-shadow': '0px 0px 19px #999',
                'padding': '30px 30px 30px 30px',
                'z-index': 20,
                
                delayFade: 4 * 1000,
                fadeTime:  0.5 * 1000,
        };
        
        if (feedback.alertTypes[type] != undefined) {
            common.merge(cssParams, feedback.alertTypes[type]);            
        }
        common.merge(cssParams, params);
        var delayFade = cssParams.delayFade;
        var fadeTime = cssParams.fadeTime;
        delete(cssParams.delayFade);
        delete(cssParams.fadeTime);
                
        if (typeof(cssParams.top) != 'string') {
            cssParams.top = cssParams.top + 'px';
        }
                
        var tdiv = document.body;
        var alertDiv = $("<div>" + msg + "</div>")
            .attr('id', 'alertDiv')
            .css(cssParams)
            .delay(delayFade)
            .fadeOut(fadeTime, function () { this.remove(); } );
        $(tdiv).append(alertDiv);
    };
    
    feedback.glow = function ($what, size, animateTime) {
        var stepFunc = function (currentTempPropertyValue) {            
            var goldColor = "#006644";
            var computed = '0px 0px ' + currentTempPropertyValue + 'px ' + goldColor;                
            $(this).css('box-shadow', computed);
        };
        var stepFunc2 = function (currentTempPropertyValue) {            
            var goldColor = "#006644";
            var computed = '0px 0px ' + (size - currentTempPropertyValue) + 'px ' + goldColor;                
            $(this).css('box-shadow', computed);
        };
        
        var storedTextShadow = $what.css('box-shadow');
        size = size || 50;
        animateTime = animateTime || 3000;        
        $what.css('-m21j-TempProperty', 0);
        $what.animate({'-m21j-TempProperty': size}, {
            duration: animateTime,
            step: stepFunc,
            complete: function () { 
                $(this).animate({'-m21j-TempProperty': size}, {
                    duration: animateTime,
                    step: stepFunc2,   
                    complete: function () { 
                        $what.css('-m21j-TempProperty', "");
                        if (storedTextShadow !== undefined) {
                            $what.css('box-shadow', storedTextShadow);
                        } else {
                            $what.css('box-shadow', '');
                        }
                    }
                }); 
            },
        }
        );
        return $what; // passthrough..
    };

    feedback.overlay = function (appendInner, appendOuter, options) {
        var params = {
           horizontalFraction: .6,
           verticalFraction: .6,
           innerHorizontalFraction: .9,
           innerVerticalFraction: .7,
        };
        music21.common.merge(params, options);
        
        var docHeight = $(document).height();
        var $commentOverlay = $("<div class='overlay'></div>")
            .height(docHeight)
            .css({
                'opacity' : 0.6,
                'position': 'absolute',
                'top': 0,
                'left': 0,
                'background-color': 'black',
                'width': '100%',
                'z-index': 100       
            });
        var ww = $(window).width();
        var wh = $(window).height();
        var $commentBody = $("<div class='overlayBody'></div>")
           .css({
               'background-color': '#909090',
               'position': 'fixed',
               'top': wh * (1 - params.verticalFraction)/2,
               'left': ww * (1 - params.horizontalFraction)/2,
               'width': ww * params.horizontalFraction,
               'height': wh * params.verticalFraction,
               'z-index': 101,
               'border-radius': '40px',
           });
        
        var $closeButton = $("<div class='overlayCloseButton'>X</div>");
        $closeButton.on('click', function () { 
            $('.overlay').remove();
            $('.overlayBody').remove();
        });
        $closeButton.css({
            'font-size': '30px',
            'position': 'absolute',
            'top': '-50px',
            'right': '-20px',
            'background-color': 'white',
            'padding': '20px 20px 20px 20px',
            'border-radius': '20px',
            'width': '20px',
            'height': '20px',
            'opacity': 0.9,
            'border': '4px #333333 solid',
            'text-align': 'center',
            'cursor': 'pointer',
            'z-index': 102,
        });
        $commentBody.append($closeButton);
        
        if (appendInner != undefined) {
            var $commentInnerBody = $("<div></div>").css({
                width: (params.innerHorizontalFraction * 100).toString() + '%',
                height: (params.innerVerticalFraction * 100).toString() + '%',
                'text-align': 'center',
                'position': 'relative',
                left: '5%',
                top: '5%',
                'border-radius': '10px',
                'padding-top': '20px',
                'background-color': 'white',
                border: '2px #999999 solid',
                overflow: 'auto',
            });
            $commentInnerBody.append(appendInner);
            $commentBody.append($commentInnerBody);
        }         
        
        if (appendOuter != undefined) {
            $commentBody.append(appendOuter);
        }
        
        $("body").append($commentOverlay);
        $("body").append($commentBody);
        return $commentBody;
    };
    return feedback;
    
});