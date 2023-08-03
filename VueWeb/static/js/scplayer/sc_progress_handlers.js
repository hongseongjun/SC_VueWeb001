//*********************************************************************************************************************
//  Control [Progress Bar] of [normalize_selected_items] Action in Django Admin [Changelist], 2021.09.15
//*********************************************************************************************************************

window.addEventListener("load", function() {
  (function($) {
    "use strict";

    // 1) Get Tags of Admin Changelist
    //var form = $('#changelist-form');
    //var inputs = $('#changelist-form select').not('.action-select,#action-toggle,[name=action]').not('[type=hidden],[type=submit]');
    var submit = $('[type=submit]');                    //Get Submit Tag
    var m_init = false;                                 //Set Progress not to be Done
    $('#progress').hide();                              //Set Progress to Hide State

    // 2) Set Action Submit Handler of Admin Changelist
    submit.click(function () {
      // (1) Get Select('normalize_selected_items') of Admin Changelist
      var selects = $('#changelist-form select');
      if (selects.val() != 'normalize_selected_items') {
        return;
      }

      // (2) Set Function to get Progress State Information from Server by Ajax
      var get_ajax = function() {
        fetch('sc_admin_progress/')
          .then(function(response) {
            if(response.ok) {
              return response.json();
            }
            throw new Error('Network response was not ok.');
          })
          .then(function(myJson) {
            //(2.1) Get Value & Max of Progress Bar from Server, and then Set Progress Bar
            var m_Dic = JSON.parse(JSON.stringify(myJson));
            if (m_init) {                       //Set Value of Progress Bar
              $('#progress').val(m_Dic['progress_val']);
            }
            else {                              //Set Initialization of Progress Bar
              //if (m_Dic['progress_total'] != 100000) {
              if (m_Dic['progress_max']) {
                m_init = true;              //Set Progress to be Done
                $('#progress').attr('max', m_Dic['progress_max']);
                $('#progress').val(m_Dic['progress_val']);
                $('#progress').show();
              }
            }
            //(2.2) Clear setInterval()
            if (m_Dic['progress_val'] == m_Dic['progress_max']) {
              m_init = true;                  //Set Progress not to be Done
              $('#progress').hide();
              clearInterval(sc_loop);         //Clear setInterval()
            }
          })
          .catch(function(error) {
            console.log('There has been a problem with your fetch operation: ', error.message);
          });
        }

      // (3) Get repeatedly State Information of Progress Bar from Server by Ajax
      var sc_loop = setInterval(get_ajax, 500);
    });
  })(django.jQuery);
});