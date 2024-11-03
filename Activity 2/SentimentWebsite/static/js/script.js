// Sample data structure for Bitcoin prices
const data = [
    { date: new Date('2024-10-21'), open: 60000, high: 60500, low: 59500, close: 60200 },
    { date: new Date('2024-10-22'), open: 60200, high: 61000, low: 59800, close: 60800 },
    // Add more data points as needed
];

// Set the dimensions of the canvas
const margin = { top: 20, right: 30, bottom: 40, left: 50 };
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// Create the SVG canvas
const svg = d3.select("#btc-chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Set the scales
const x = d3.scaleBand()
    .domain(data.map(d => d.date))
    .range([0, width])
    .padding(0.2);

const y = d3.scaleLinear()
    .domain([d3.min(data, d => d.low), d3.max(data, d => d.high)])
    .range([height, 0]);

// Create axes
svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%Y-%m-%d")));

svg.append("g")
    .attr("class", "y-axis")
    .call(d3.axisLeft(y));

// Draw candlesticks
svg.selectAll(".candlestick")
    .data(data)
    .enter()
    .append("g")
    .attr("class", "candlestick")
    .attr("transform", d => `translate(${x(d.date)},0)`)

    // Create the line for high and low
    .append("line")
    .attr("y1", d => y(d.high))
    .attr("y2", d => y(d.low))
    .attr("stroke", d => d.open > d.close ? "red" : "green")
    .attr("stroke-width", 2)
    .attr("x1", 0)
    .attr("x2", 0);

svg.selectAll(".candlestick")
    .append("rect")
    .attr("y", d => d.open > d.close ? y(d.open) : y(d.close))
    .attr("height", d => Math.abs(y(d.open) - y(d.close)))
    .attr("width", x.bandwidth())
    .attr("fill", d => d.open > d.close ? "red" : "green");

