/* Editor Code */
var aceRange = ace.require("ace/range").Range;
var editor = null;
var marker = null;

function removeMarker() {
    if (marker !== null) {
        editor.getSession().removeMarker(marker);
        marker = null;
    }
}

function annotateLine(line, type) {
    removeMarker();
    marker = editor.getSession().addMarker(
        new aceRange(line, 0, line, 10),
        "highlight",
        "fullLine",
        true
    );
    editor.getSession().setAnnotations([{row: line, type: type}]);
}

function clearAnnotations() {
    removeMarker();
    editor.getSession().clearAnnotations();
}


/* Graph Code */
var svg = null, force = null, nodes = null, links = null;

d3.selection.prototype.moveToFront = function () {
    return this.each(function () {
        this.parentNode.appendChild(this);
    });
};

function resize() {
    var width = window.innerWidth / 2, height = window.innerHeight;
    svg.attr("width", width).attr("height", height);
    force.size([width, height]).resume();
}

function dragstart(d) {
    d.fixed = true;
    d3.select(this).classed("fixed", d.fixed);
}

function dblclick(d) {
    d.fixed = false;
    d3.select(this).classed("fixed", d.fixed);
}

function getId(d) {
    return d.id;
}

function getLabel(d) {
    return d.label;
}

function update_graph(graph) {
    var i, j, found, link, node, nodeEnter;

    if (graph.error_line !== undefined) {
        annotateLine(graph.error_line - 1, "error");
        return;
    }
    clearAnnotations();

    for (i = 0; i < graph.nodes.length; i += 1) {
        found = false;
        for (j = 0; j < nodes.length; j += 1) {
            if (nodes[j].id === graph.nodes[i].id) {
                found = true;
                nodes[j].label = graph.nodes[i].label;
                nodes[j].line = graph.nodes[i].line;
            }
        }
        if (!found) {
            nodes.push(graph.nodes[i]);
        }
    }

    for (j = 0; j < nodes.length; j += 1) {
        found = false;
        for (i = 0; i < graph.nodes.length; i += 1) {
            if (nodes[j].id === graph.nodes[i].id) {
                found = true;
            }
        }
        if (!found) {
            nodes.splice(j, 1);
            j -= 1;
        }
    }

    links.splice(0, links.length);
    for (i = 0; i < graph.links.length; i += 1) {
        links.push(graph.links[i]);
    }

    link = svg.selectAll(".link").data(links, getId);
    link.enter().append("polyline").attr("class", "link").attr("id", getId);
    link.exit().remove();

    node = svg.selectAll("g.node").data(nodes, getId);
    nodeEnter = node
        .enter()
        .append("g")
        .attr("class", "node")
        .on("dblclick", dblclick)
        .on("mouseover", function (d) {annotateLine(d.line, "info"); })
        .on("mouseout", function (d) {clearAnnotations(); })
        .call(force.drag);
    nodeEnter
        .append("circle")
        .attr("r", "20")
        .attr("id", function (d) {return "Node;" + d.id; });
    nodeEnter.append("text").text(getLabel);
    node.exit().remove();

    svg.selectAll("g.node").data(nodes, getId).selectAll("text").text(getLabel);
    svg.selectAll("g.node").data(nodes, getId).moveToFront();

    force.on("tick", function () {
        link.attr("points", function (d) {
            return d.source.x + "," + d.source.y + " " +
                   (d.source.x * 0.45 + d.target.x * 0.55) + "," +
                   (d.source.y * 0.45 + d.target.y * 0.55) + " " +
                    d.target.x + "," + d.target.y;
        });
        node.attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")";
        });
    });

    resize();
    force.linkDistance(100).start();
}

function fetch_graph() {
    $.getJSON("model", {"code": editor.getValue()}, update_graph);
}


/* Simulation Streaming Code */
function stream() {
    $.stream("simulate", {
        type: "http",
        dataType: "json",
        openData: {
            code: editor.getValue()
        },
        message: function (event) {
            $("#simulation #time").text(event.data.t.toFixed(3));
            var probe_data = [];
            $.each(event.data.probes, function (probe, x) {
                probe_data.push(probe + "=" + x);
            });
            $("#simulation #probes").text(probe_data.join("\n"));
        }
    });
}


$(document).ready(function () {
    /* Initialize editor */
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.on("change", function (e) {
        fetch_graph();
    });

    /* Initialize graph */
    svg = d3.select("svg");
    force = d3.layout.force();
    nodes = force.nodes();
    links = force.links();
    force.charge(-100);
    force.drag().on("dragstart", dragstart);
    d3.select(window).on("resize", resize);

    /* Initialize simulation handlers */
    $("#button-play").click(function () {
        $(this).hide();
        stream();
    });

    /* Go! */
    fetch_graph();
});
