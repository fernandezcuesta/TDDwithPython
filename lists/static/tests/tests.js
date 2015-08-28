/* global $, test, equal */
//test( "smoke test", function( ) {
//  equal($('.has-error').is(':visible'), true);
//  $('.has-error').hide();
//  equal($('.has-error').is(':visible'), false);
//});



QUnit.test( "error should be hidden on keypress", function( assert ) {
  $('input').trigger('keypress');
  assert.notOk($('.has-error').is(':visible'), "Error hidden" );
});

QUnit.test( "error should not be hidden until keypress", function( assert ) {
  assert.ok($('.has-error').is(':visible'), "Error visible" );
});
