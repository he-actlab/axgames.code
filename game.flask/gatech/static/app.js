var main = function() {

	$('.carousel').carousel({
		interval: false
	});

	$('#thumbnail-display').click(function() {
		$('.thumb').fadeIn(1600);
		$('.caption').fadeIn(1600);
		$('#thumbnail-display').hide();
	});
	
	$('#level-aux').hide();
	$('#level-chips').hide();
	$('#level-betting-money').hide();
	$('#level-six-buttons').hide();
	$('#level-bankroll').hide();	
	
	$('#level-main').click(function() {
		$('#level-main').fadeOut(600).promise().done(function() {
			$('#level-aux').fadeIn(1600);
			$('#level-chips').fadeIn(1600);
			$('#level-betting-money').fadeIn(1600);
			$('#level-six-buttons').fadeIn(1600);
			$('#level-bankroll').fadeIn(1600);
 		});
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
