// Move to V4
// https://bl.ocks.org/shimizu/e6209de87cdddde38dadbb746feaf3a3
// https://bl.ocks.org/wnghdcjfe/c2b04ee8430afa32ce76596daa4d8123
//
// https://www.d3-graph-gallery.com/graph/interactivity_zoom.html

var width = 2048;
var height = 600;

var color = d3.scaleOrdinal(d3.schemeCategory20);

var force = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.index }))
    .force("collide",d3.forceCollide( function(d){return d.r + 8 }).iterations(16) )
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("y", d3.forceY(0))
    .force("x", d3.forceX(0))


var svg = d3.select("#graph")
  .append("svg")
    .attr("width",  width)
    .attr("height",  height)
    .call(d3.zoom().on("zoom", function () {
       svg.attr("transform", d3.event.transform)
    }))
  .append("g")

d3.json("eguk_authorship_network.json", function(error,json)
{
    if (error) throw error;

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.index }))
        .force("collide",d3.forceCollide( function(d){return d.r + 8 }).iterations(2) )
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("y", d3.forceY(0))
        .force("x", d3.forceX(0))

    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
            .data(json.links)
            .enter()
                .append("line")
                .attr("class", "link")
                .style("stroke-width", function(d) { return (1.5 * d.weight); });

    var node = svg.append("g")
        .attr("class", "node")
        .selectAll("circle")
            .data(json.nodes)
            .enter()
            // .append("text")
            // .attr("class", "text")
            // .attr('x', 6)
            // .attr('y', 3)
            // .text(function(d) { return d.name })
                .append("circle")
                .attr("class", "nodes")
                .attr("r", function(d){  return d.publications * 2 })
                .style("fill", function(d) { return color(d.group); })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended))
                    .on("click", nodeClicked)
                       //
    // var labels = svg.append("g")
    //     .attr("class", "text")
    //     .selectAll("text")
    //         .data(json.nodes)
    //         .enter()
    //             .append("text")
    //             .attr('x', 6)
    //             .attr('y', 3)
    //             // .attr("dx", 12)
    //             // .attr("dy", ".35em")
    //             // .attr("stroke", "black")
    //             .text(function(d) { return d.name });


    simulation
    .nodes(json.nodes)
    .on("tick", ticked);

    simulation.force("link")
    .links(json.links);

    //svg.selectAll("node").on("click", function(id) { var _node = g.node(id); console.log("Clicked " + id,_node); });


    function ticked() {
      link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node
          .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
          })
    }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;

    element = d3.select(this);

    d.old_r      = element.attr("r");
    d.old_fill   = element.attr("fill");
    d.old_stroke = element.attr("stroke");

    element.attr("r", d.old_r * 1.5);
    element.attr("fill","lightcoral");
    element.attr("stroke","red");
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;

    element = d3.select(this);

    element.attr('r',      d.old_r);
    element.attr("fill",   d.old_fill);
    element.attr("stroke", d.old_stroke);
  }

  function nodeClicked(d) {
      element = d3.select(this);
      console.log(d);
  }
});
