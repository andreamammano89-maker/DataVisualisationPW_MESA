var cities = {
  Rome: {
    price: '132 EUR', priceSub: 'lower than Copenhagen',
    avail: '260 days', availSub: '71% of the year',
    d180: '68.1%', d180Sub: 'near full-time operation',
    upi: '0.27', upiSub: 'urban pressure index',
    dom: '39.2%', domSub: 'held by top 10% of hosts',
    casual: 41.6, semi: 29.0, pro: 29.4,
    color: '#8B3A2A',
    insight: 'In Rome, professional hosts are only 5.1% of all hosts yet control <strong>29.4% of all listings</strong>. The top 1% of hosts alone control 13.9% of the market. Combined with semi-professional hosts, 58.4% of Rome\'s supply is managed by multi-listing operators.'
  },
  Copenhagen: {
    price: '161 EUR', priceSub: 'higher than Rome',
    avail: '115 days', availSub: '31% of the year',
    d180: '38.4%', d180Sub: 'more occasional use',
    upi: '0.44', upiSub: 'urban pressure index',
    dom: '20.0%', domSub: 'held by top 10% of hosts',
    casual: 85.3, semi: 6.9, pro: 7.8,
    color: '#2A5C45',
    insight: 'In Copenhagen, casual hosts manage <strong>85.3% of all listings</strong>. The top 1% of hosts control just 9.1% of the market. Professional hosts account for only 7.8% of supply, reflecting a market still close to the peer-to-peer model.'
  }
};

function setCity(city) {
  var d = cities[city];
  document.getElementById('btn-rome').className = 'city-btn' + (city === 'Rome' ? ' active' : '');
  document.getElementById('btn-cop').className  = 'city-btn' + (city === 'Copenhagen' ? ' active' : '');
  document.getElementById('val-price').textContent = d.price;
  document.getElementById('sub-price').textContent = d.priceSub;
  document.getElementById('val-avail').textContent = d.avail;
  document.getElementById('sub-avail').textContent = d.availSub;
  document.getElementById('val-180').textContent = d.d180;
  document.getElementById('sub-180').textContent = d.d180Sub;
  document.getElementById('val-upi').textContent = d.upi;
  document.getElementById('sub-upi').textContent = d.upiSub;
  document.getElementById('val-dom').textContent = d.dom;
  document.getElementById('sub-dom').textContent = d.domSub;
  document.getElementById('bar-casual').style.width = d.casual + '%';
  document.getElementById('pct-casual').textContent = d.casual.toFixed(1) + '%';
  document.getElementById('bar-semi').style.width = d.semi + '%';
  document.getElementById('pct-semi').textContent = d.semi.toFixed(1) + '%';
  document.getElementById('bar-pro').style.width = d.pro + '%';
  document.getElementById('pct-pro').textContent = d.pro.toFixed(1) + '%';
  document.getElementById('exp-insight').style.borderColor = d.color;
  document.getElementById('insight-text').innerHTML = d.insight;
}

var hats = {
  white: {
    img: 'https://romevscopenhagen.wpcomstaging.com/wp-content/uploads/2026/05/white_hat.jpg',
    alt: 'White hat scatter plot showing professional host share vs UPI for Rome and Copenhagen',
    title: 'White hat: honest representation',
    desc: 'Scatter plot with confidence intervals, correlation statistics, and a causal disclaimer · Both cities',
    border: '#2A5C45',
    text: '<strong>Why this is white hat:</strong> Both cities are shown simultaneously, preventing selective presentation of the stronger result. Both axes are anchored at zero. Ninety-five percent confidence intervals are shaded around each regression line. Pearson correlation coefficients and p-values are annotated directly on the chart. The caption states explicitly that correlation does not imply causation and identifies the UPI as an author-constructed composite.'
  },
  black: {
    img: 'https://romevscopenhagen.wpcomstaging.com/wp-content/uploads/2026/05/black_hat.jpg',
    alt: 'Black hat dual-axis line chart implying causation between professionalisation and urban pressure',
    title: 'Black hat: misleading representation',
    desc: 'Dual-axis line chart with engineered ordering that implies causation · Copenhagen only',
    border: '#8B3A2A',
    text: '<strong>Why this is black hat:</strong> The chart shows only Copenhagen, hiding the weaker Rome correlation. Two independent y-axes are scaled so the lines appear to move in lockstep. Neighbourhoods are sorted by the average of their UPI rank and professional host share rank, maximising visual co-movement. No confidence intervals or causal disclaimers are included. Every data point is accurate, but the design produces an impression that far exceeds what the data supports.'
  }
};

function setHat(hat) {
  var d = hats[hat];
  document.getElementById('btn-white').className = 'city-btn' + (hat === 'white' ? ' active' : '');
  document.getElementById('btn-black').className = 'city-btn' + (hat === 'black' ? ' active' : '');
  var img = document.getElementById('hat-image');
  img.style.opacity = '0';
  setTimeout(function() {
    img.src = d.img;
    img.alt = d.alt;
    img.style.opacity = '1';
  }, 150);
  document.getElementById('hat-viz-title').textContent = d.title;
  document.getElementById('hat-viz-desc').textContent = d.desc;
  document.getElementById('hat-explanation').style.borderColor = d.border;
  document.getElementById('hat-explanation').innerHTML = d.text;
}
