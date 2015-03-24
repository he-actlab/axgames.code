var main = function() {

	$('.carousel').carousel({
		interval: false
	});
	
	//$('.thumb').hide();
	//$('.thumb').fadeIn(2600);
	//$('.caption').hide();

	$('#thumbnail-display').click(function() {
		$('.thumb').fadeIn(1600);
		$('.caption').fadeIn(1600);
		$('#thumbnail-display').hide();
	});
	
	$('#level-aux').hide();
	$('#level-chips').hide();
	$('#level-betting-money').hide();
	$('#level-three-buttons').hide();
	$('#level-bankroll').hide();
	
	$('#level2-aux').hide();
	$('#level2-chips').hide();
	$('#level2-betting-money').hide();
	$('#level2-three-buttons').hide();
	$('#level2-bankroll').hide();
	
	$('#level3-aux').hide();
	$('#level3-chips').hide();
	$('#level3-betting-money').hide();
	$('#level3-three-buttons').hide();
	$('#level3-bankroll').hide();
	
	
	
	
	$('#level-main').click(function() {
		$('#level-main').fadeOut(600);
		$('#level-aux').fadeIn(1200);
		$('#level-chips').fadeIn(1200);
		$('#level-betting-money').fadeIn(1200);
		$('#level-three-buttons').fadeIn(1200);
		$('#level-bankroll').fadeIn(1200);
	});
	
	$('#level2-main').click(function() {
		$('#level2-main').fadeOut(600);
		$('#level2-aux').fadeIn(1200);
		$('#level2-chips').fadeIn(1200);
		$('#level2-betting-money').fadeIn(1200);
		$('#level2-three-buttons').fadeIn(1200);
		$('#level2-bankroll').fadeIn(1200);
	});
	
	$('#level3-main').click(function() {
		$('#level3-main').fadeOut(600);
		$('#level3-aux').fadeIn(1200);
		$('#level3-chips').fadeIn(1200);
		$('#level3-betting-money').fadeIn(1200);
		$('#level3-three-buttons').fadeIn(1200);
		$('#level3-bankroll').fadeIn(1200);
	});
	
	var betMoney = 0;
	
	$('#bet5').click(function() {
		betMoney = betMoney + 5;
		$('#bet-money').text('Bet: $' + betMoney);
	});
	
	$('#bet25').click(function() {
		betMoney = betMoney + 25;
		$('#bet-money').text('Bet: $' + betMoney);
	});
	
	$('#bet100').click(function() {
		betMoney = betMoney + 100;
		$('#bet-money').text('Bet: $' + betMoney);
	});
	
	$('#bet500').click(function() {
		betMoney = betMoney + 500;
		$('#bet-money').text('Bet: $' + betMoney);
	});
	
	$('#bet1000').click(function() {
		betMoney = betMoney + 1000;
		$('#bet-money').text('Bet: $' + betMoney);
	});
	
	$('#bet5000').click(function() {
		betMoney = betMoney + 5000;
		$('#bet-money').text('Bet: $' + betMoney);
	});

	$('#clear').click(function() {
		betMoney = 0;
		$('#bet-money').text('Bet: $' + betMoney);
	});

};

$(document).ready(main);
