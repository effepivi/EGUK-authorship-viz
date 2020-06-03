// Move to V4
// https://bl.ocks.org/shimizu/e6209de87cdddde38dadbb746feaf3a3
// https://bl.ocks.org/wnghdcjfe/c2b04ee8430afa32ce76596daa4d8123
//
// https://www.d3-graph-gallery.com/graph/interactivity_zoom.html

var width = 2048;
var height = 600;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(100)
    .size([width, height]);

var svgnode = d3.select("#header1").append("svg")
    .attr("width", width)
    .attr("height", height);



d3.json("eguk_authorship_network.json", function(error,json)
{
    if (error) throw error;

    force
        .nodes(json.nodes)
        .links(json.links)
        .start();

    var link = svgnode.selectAll(".link")
        .data(json.links)
        .enter().append("line")
        .attr("class", "link")
        //.style("stroke-width", function(d) { return Math.sqrt(d.weight); });

    var node = svgnode.selectAll(".node")
        .data(json.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(force.drag);

    node.append("circle")
        .attr("r", function(d) {
            d.weight = link.filter(function(l) {
                return l.source.index == d.index || l.target.index == d.index
            }).size();
            var minRadius = 5;
            return minRadius + (d.publications * 2);
        })
        .style("fill", function(d) { return color(d.group); })

    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });
});
