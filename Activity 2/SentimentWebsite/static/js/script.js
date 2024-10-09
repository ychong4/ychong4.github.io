document.addEventListener('DOMContentLoaded', function () {
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#btc-chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const xScale = d3.scaleLinear().range([0, width]);
    const yScale = d3.scaleLinear().range([height, 0]);
    const line = d3.line()
        .x((d, i) => xScale(i))
        .y(d => yScale(d));

    let prices = [];
    let currentPrice = null;

    const xAxisGroup = svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height})`);
    
    const yAxisGroup = svg.append("g")
        .attr("class", "y-axis");

    function updateChart(price) {
        // Update the current price
        currentPrice = price;

        prices.push(price);
        // Keep the last 50 prices to create a rolling window
        if (prices.length > 50) {
            prices.shift(); // Remove the oldest price
        }

        // Update the scales
        xScale.domain([0, prices.length - 1]);
        const minPrice = currentPrice - 100;
        const maxPrice = currentPrice + 100;
        yScale.domain([minPrice, maxPrice]);

        // Bind data and create/update the line
        svg.selectAll(".line").remove(); // Remove existing line
        svg.append("path")
            .datum(prices) // Bind the prices data
            .attr("class", "line")
            .attr("d", line); // Generate the path

        // Update axes
        xAxisGroup.call(d3.axisBottom(xScale).ticks(prices.length));
        yAxisGroup.call(d3.axisLeft(yScale));
    }

    const socket = new WebSocket('wss://ws.finnhub.io?token=crvli3hr01qkji45lrj0crvli3hr01qkji45lrjg');

    socket.addEventListener('open', function (event) {
        console.log("WebSocket connection established.");
        socket.send(JSON.stringify({ 'type': 'subscribe', 'symbol': 'BINANCE:BTCUSDT' }));
    });

    socket.addEventListener('message', function (event) {
        const message = JSON.parse(event.data);
        console.log('Message from server: ', message);

        // Check if the message is of type 'trade' and contains data
        if (message.type === 'trade' && message.data && message.data.length > 0) {
            // Extract the price from the latest trade data
            const latestTrade = message.data[message.data.length - 1]; // Get the last trade
            const price = latestTrade.p; // Extract the price

            if (price) { // Check if the price is valid
                console.log(`Current BTC Price: $${price}`);
                updateChart(price); // Update the chart with the latest price
            }
        } else if (message.type === 'ping') {
            console.log("Received ping, sending pong.");
            socket.send(JSON.stringify({ "type": "pong" }));
        }
    });
});
