function Header(el) {
    this.el = el;
    var is_firefox = navigator.userAgent.indexOf("Firefox") ;  // by I8FUC 
    
    var $buttons = this.el.find('.openwebrx-main-buttons').find('[data-toggle-panel]').filter(function(){
        // ignore buttons when the corresponding panel is not in the DOM
        return $('#' + $(this).data('toggle-panel'))[0];
    });


    if (navigator.userAgent.indexOf("Firefox") >= 0){  // by I8FUC to support correct top bar buttons hiding on firefox derived browsers
      $buttons.css({display: 'block'}).click(function () {    
        toggle_panel($(this).data('toggle-panel'));
        });
      }
    else{
      $buttons.click(function () {    
        toggle_panel($(this).data('toggle-panel'));
        });    
      };    

    this.init_rx_photo();
};

Header.prototype.setDetails = function(details) {
    this.el.find('.webrx-rx-title').html(details['receiver_name']);
    this.el.find('.webrx-rx-desc').html(details['receiver_location'] + ' | Loc: ' + details['locator'] + ', ASL: ' + details['receiver_asl'] + ' m');
    this.el.find('.webrx-rx-photo-title').html(details['photo_title']);
    this.el.find('.webrx-rx-photo-desc').html(details['photo_desc']);
};

Header.prototype.init_rx_photo = function() {
    this.rx_photo_state = 0;

    $.extend($.easing, {
        easeOutCubic:function(x) {
            return 1 - Math.pow( 1 - x, 3 );
        }
    });

    $('.webrx-top-container').find('.openwebrx-photo-trigger').click(this.toggle_rx_photo.bind(this));
    $('.webrx-top-container-black').find('.openwebrx-photo-trigger').click(this.toggle_rx_photo.bind(this));  // by I8FUC to support ivanmarcus black_mod   
};

Header.prototype.close_rx_photo = function() {
    this.rx_photo_state = 0;
    this.el.find('.openwebrx-description-container').removeClass('expanded');
    this.el.find(".openwebrx-rx-details-arrow").removeClass('openwebrx-rx-details-arrow--up').addClass('openwebrx-rx-details-arrow--down');
}

Header.prototype.open_rx_photo = function() {
    this.rx_photo_state = 1;
    this.el.find('.openwebrx-description-container').addClass('expanded');
    this.el.find(".openwebrx-rx-details-arrow").removeClass('openwebrx-rx-details-arrow--down').addClass('openwebrx-rx-details-arrow--up');
}

Header.prototype.toggle_rx_photo = function(ev) {
    if (ev && ev.target && ev.target.tagName == 'A') {
        return;
    }
    if (this.rx_photo_state) {
        this.close_rx_photo();
    } else {
        this.open_rx_photo();
    }
};

$.fn.header = function() {
    if (!this.data('header')) {
        this.data('header', new Header(this));
    }
    return this.data('header');
};

$(function(){
    $('.webrx-top-container').header();
    $('.webrx-top-container-black').header();  // by I8FUC to support ivanmarcus black_mod
});
