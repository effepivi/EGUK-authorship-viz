// Move to V4
// https://bl.ocks.org/shimizu/e6209de87cdddde38dadbb746feaf3a3
// https://bl.ocks.org/wnghdcjfe/c2b04ee8430afa32ce76596daa4d8123
//
// https://www.d3-graph-gallery.com/graph/interactivity_zoom.html


var graph_element = d3.select('#graph').node();

var width = Math.floor(graph_element.getBoundingClientRect().width);
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


var authorship;
var articles;
var conferences;

function recordAuthorship(json) {
    authorship = json;
}

function recordArticles(json) {
    articles = json;
}

function recordConferences(json) {
    conferences = json;
}

fetch("authorship.json")
    .then(response => response.json())
    .then(json => recordAuthorship(json))

fetch("articles.json")
    .then(response => response.json())
    .then(json => recordArticles(json))

fetch("conferences.json")
    .then(response => response.json())
    .then(json => recordConferences(json))




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
            // Trying to add text next to the nodes with offset (x,y)
            // Failling to add the translation to both circle and text.
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
                    //.on("click", nodeClicked) // Not needed as taken care by dragstarted
                       //

                       // Trying to add text next to the nodes with offset (x,y)
                       // Failling to add the translation to both circle and text.
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

    function dragstarted(d)
    {
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

        nodeClicked(d);
    }

    function dragged(d)
    {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d)
    {
        if (!d3.event.active) simulation.alphaTarget(0);

        d.fx = null;
        d.fy = null;

        element = d3.select(this);

        element.attr('r',      d.old_r);
        element.attr("fill",   d.old_fill);
        element.attr("stroke", d.old_stroke);
    }


    function getArticleByAuthorID(author_id)
    {
        return authorship.filter(
            function(authorship){ return authorship.author_id == author_id }
        );
    }

    function getArticleByID(article_id)
    {
        return articles.filter(
            function(articles){ return (articles.id == article_id) }
        );
    }

    function getConferenceByID(conference_id)
    {
        return conferences.filter(
            function(conferences){ return (conferences.id == conference_id) }
        );
    }

    function nodeClicked(d)
    {
        var fieldNameElement = document.getElementById('side_panel');

        //var side_panel = d3.select("#side_panel")

        article_ids = getArticleByAuthorID(d.index + 1);
        text = "<p>Author: " + d.name;
        if (article_ids.length == 1)
        {
            text += ": " + article_ids.length + " article";
        }
        else
        {
            text += ": " + article_ids.length + " articles";
        }
        text += "</p><p><ul>";

        for (i = 0; i < article_ids.length; ++i)
        {
            article_id = article_ids[i].paper_id;
            article = getArticleByID(article_id)[0];

            conference_id = article.conference_id;
            conference = getConferenceByID(conference_id)[0];

            text += "<li>" + article.title + " in <i>Proceedings of " + conference.short_name + conference.year + "</li>";
        }
        text += "</ul></p>";

        // $("side_panel").update(text);
        fieldNameElement.innerHTML = text;
        // side_panel.text(text);
    }
});
