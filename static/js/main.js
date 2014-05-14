//*****************
// Setup the editor
//*****************
//Functions for interaction with editor
var aceRange = ace.require('ace/range').Range;
var editor = null;
var marker = null;
var gui_updating = false;

function removeMarker() {
    if (marker != null) {
        editor.getSession().removeMarker(marker);
        marker = null;
    }
}

function annotateLine(d) { //Called on mouseover in graph
    removeMarker();
    marker = editor.getSession()
        .addMarker(new aceRange(d.line, 0, d.line, 10), 
            'highlight', 'fullLine', true);

    editor.getSession().setAnnotations([{row: d.line, type: 'info'}]);
}

function clearAnnotation(d) { //Called on mouseout in graph
    removeMarker();
    editor.getSession().clearAnnotations();
}

//***********************
// Setup the file browser
//***********************
//Load the browser and hide it

function open_file(file) {
    $('#filebrowser').hide();

    container.selectAll('.link').remove();
    container.selectAll('.node').remove();
    editor.setValue('');

    var data = new FormData();
    data.append('filename', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/openfile', true);
    xhr.onload = function (event) {editor.setValue(this.responseText);};
    xhr.send(data);
}

function update_gui_pos() {
    gui_updating = true;
    var pos = '\nimport nengo_gui\ngui = nengo_gui.Config()\n';
    for (var i=0; i<graph.nodes.length; i++) {
        d = graph.nodes[i];
        pos += "gui[" + d.id + "].pos = " + d.x + ", " + d.y + "\n";
    }
    
    text = editor.getValue();
    index = text.indexOf('\nimport nengo_gui\n');
    if (index!=-1) {
        text = text.substring(0, index);
    }
    
    new_text = text + pos;
    
    editor.session.setValue(new_text);
    gui_updating = false;    
}
//*****************
// Helper functions
//*****************

//**************
// Drag and zoom
//**************
function dragstarted(d) {
    d3.event.sourceEvent.stopPropagation();
    d3.select(this).classed("dragging", true);
}

function dragged(d) {
    //console.log(d.x, d3.event.dx)
    dx = d3.event.dx
    dy = d3.event.dy
    if (d.type == 'net' || d.contained_by == -1) {
        d.x = d.x + dx;
        d.y = d.y + dy;

        d3.select(this)
            .attr('transform', "translate(" + [d.x, d.y] 
                + ")scale(" + this.zoom.scale() + ')');
    }
    
    //sort the nodes by size of full contains (largest to smallest)
    //var node_list = graph.nodes.slice(0)
    //node_list.sort(containsCompare);
    //node_list = d3.map(node_list); //create a map of the nodes
    //update_node_positions(d, d3.event.dx, d3.event.dy, node_list);
    //update_subnet_position(d, d3.event.dx, d3.event.dy);
    update_net_size(d, dx, dy);
    update_line_locations();
    update_gui_pos();
}

function dragended(d) {
    d3.select(this).classed("dragging", false);
}

function zoomed(d) {
    d3.event.sourceEvent.stopPropagation();
    scale = d3.event.scale;
    translate = d3.event.translate;
    
    if (typeof d == 'undefined') {
        //called at the top level
        thisNetwork = container;
        thisNetwork.attr("transform", function (d) { //scale & translate everything
            return "translate(" + translate + ")scale(" + scale + ")"
        })
    } else {
        thisNetwork = d3.select(this);
        thisNetwork.attr("transform", function (d) { //scale & translate everything
            return "translate(" + [d.x+translate[0], d.y+translate[1]] 
            + ")scale(" + scale + ")"  
        });
    }
    
    

    
    thisNetwork.selectAll('text') //Change the fonts size as a fcn of scale
        .style("font-size", function (d) {
            newsize = node_fontsize / scale
            if (newsize > node_fontsize) {
                return newsize + "px";
            } else {
                return node_fontsize + "px";
            }
        })

    //could be faster if keep track of whether it was just drawn
    if (scale < .75) { //Don't draw node/ens text if scale out far 
        thisNetwork.selectAll(".node_ens text, .node_nde text")
            .text("")
    } else {
        thisNetwork.selectAll(".node_ens text, .node_nde text")
            .text(function (d) {return d.label;});
    }

    //do text later
    //update_net_text();
    //update_net_sizes();
}

//***********************
// Drawing graph elements
//***********************
// Move objects to be drawn on top
var net_widths = {};
var net_heights = {};
var net_text_margin = 10;

d3.selection.prototype.moveToFront = function () {
    return this.each(function () {this.parentNode.appendChild(this);});
};

// put nodes on top, lowest level nets 2nd, and so on
function layer_container() {
    //if we had a list of what's 'contained' (i.e top level only) 
    //by model from the server, this would be more efficient
    for (var i in graph.nodes) {
        if (graph.nodes[i].type == "net") {
            layer_network(graph.nodes[i])
        }
    }

    container.selectAll('g.node').filter(function (d) {return d.type != 'net';})
        .moveToFront();
}

//Move all the nodes in a network if network position changes
function layer_network(curNode) {
    if (curNode.type == "net") {
        container.selectAll('g.node').filter(function (d) {return d == curNode;})
            .moveToFront()

        for (var obj in curNode.contains) {
            if (graph.nodes[curNode.contains[obj]].type == "net") {
                layer_network(graph.nodes[curNode.contains[obj]])
            }
        }
    }
}

function update_line_locations() {
    link.filter(function (d) {return d.type == 'std';})
        .attr('points', function (d) {
            source = nodes.filter(function (a) {
                return a == graph.nodes[d.source]})
            target = nodes.filter(function (a) {
                return a == graph.nodes[d.target]})

            x0 = source[0][0].getCTM().e;
            y0 = source[0][0].getCTM().f;
            x1 = target[0][0].getCTM().e;
            y1 = target[0][0].getCTM().f;
            return "" + x0 + "," + y0 + " " + 
                (x0 * 0.45 + x1 * 0.55) + "," + 
                (y0 * 0.45 + y1 * 0.55) + " " +
                x1 + "," + y1;
        });

    linkRecur
        .attr('x', function (d) {return graph.nodes[d.source].x})
        .attr('y', function (d) {return graph.nodes[d.source].y})
}

function update_net_text() {
    node.selectAll("g.node.node_net text") //Position net text by scale
    .attr('y', function (d) {
        if (zoom.scale() < 1) {
            return net_heights[d.id] / 2 + net_text_margin / zoom.scale() + "px"
        } else {
            return net_heights[d.id] / 2 + net_text_margin + "px"
        }
    })
}

//Update given network size based on node position
function update_net_size(d, dx, dy) {
    if (d.contained_by != -1) {
        net = graph.nodes[d.contained_by]

        xstart = 0 //middle of the network
        ystart = 0
        x0 = graph.nodes[net.contains[0]].x; //first item in net x,y as a start
        x1 = x0;
        y0 = graph.nodes[net.contains[0]].y;
        y1 = y0;
        for (obj in net.contains) { //min/max of y and x of nodes in net
            xBorder = 0
            yBorder = 0
            tmp = graph.nodes[net.contains[obj]]
            if (tmp.type == "net") {
                xBorder = net_widths[tmp.id] / 2 - net_inner_margin
                yBorder = net_heights[tmp.id] / 2 - net_inner_margin
            }
            x0 = Math.min(graph.nodes[net.contains[obj]].x - xBorder, x0);
            x1 = Math.max(graph.nodes[net.contains[obj]].x + xBorder, x1);
            y0 = Math.min(graph.nodes[net.contains[obj]].y - yBorder, y0);
            y1 = Math.max(graph.nodes[net.contains[obj]].y + yBorder, y1);
        }
        if (d.x <= x0 || d.x >= x1) {
            net.x += dx
            for (i in net.contains) {
                if (graph.nodes[net.contains[i]] != d) {
                   graph.nodes[net.contains[i]].x -= dx;
                }
            }
        }
        if (d.y <= y0 || d.y >= y1) {
            net.y += dy
            for (i in net.contains) {
                if (graph.nodes[net.contains[i]] != d) {
                   graph.nodes[net.contains[i]].y -= dy;
                }
            }
        }
        //dx = d.x - xstart;
        //dy = d.y - ystart;
        net_widths[net.id] = x1 - x0 + 2 * net_inner_margin; //track heights/widths
        net_heights[net.id] = y1 - y0 + 2 * net_inner_margin;
    
        //var node_list = graph.nodes.slice(0)
        //node_list.sort(containsCompare)
        //update_node_positions(d, 2 * dx, 2 * dy, d3.map(node_list))
    
        nets.filter(function (d) {return d.id == net.id;})
            .select('rect')
            .attr('x', function (d) {return -net_widths[net.id] / 2;})
            .attr('y', function (d) {return -net_heights[net.id] / 2;})
            .attr('width', function (d) {return net_widths[net.id];})
            .attr('height', function (d) {return net_heights[net.id];});
        
        //note: you can't translate the group you are in, so the centre of the
        //network itself can't be moved, which means this code could cause
        //the center of the net to stray far from 
    
        nets.filter(function (d) {return d.id == net.id})
            .attr('transform', function (d) {return 'translate(' + [d.x, d.y] + ')';});
        //update_net_text();
    }
}

//Move all the subnets in a network if network position changes
function update_subnet_positions(d, dx, dy) {
    for (var obj in d.contains) {
        if (graph.nodes[d.contains[obj]].type == "net") {
            graph.nodes[d.contains[obj]].x += dx
            graph.nodes[d.contains[obj]].y += dy
        }
    }
}

//Update the position of any nodes and what they affect
function update_node_positions(d, dx, dy, node_list) { //node_list must be sorted to work
    removeValue(node_list, d)
    if (d.type == 'net') { //stop all sub items from moving
        for (var i in d.full_contains) {
            node_list.remove(d.full_contains[i])
        }
    }
    for (var n in node_list.keys()) {
        var curNode = node_list.get(node_list.keys()[n])
        if (close_to(curNode, d)) {//if curNode is close to d, and not close to 
                                   //any containers of d (this is true here from sorting)
            move_node(curNode, dx, dy)
            update_node_positions(curNode, dx, dy, d3.map(node_list))
        }
    }
}

//Move the provided nodes the provided distance and note that
function move_node(node, dx, dy) {
    if (node.type == "net") { //move a network
        update_net_position(node, dx, dy)
    } else { //move ens or nde
        node.x += dx
        node.y += dy
    }
}

//Redraw if the window is resized
function resize() {
    width = window.innerWidth / 2;
    height = window.innerHeight;
    svg.attr("width", width).attr("height", height);
}

//**************
// Miscellaneous
//**************
//Remove object from a map.  Removes all matching items.
function removeValue(map, d) {
    keys = map.keys()
    for (el in map.keys()) {
        if (map.get(map.keys()[el]) == d) {
            map.remove(map.keys()[el])
        }
    }
}

// is the point x, y inside the net
function isin(d, x, y) {
    return (x < d.x + net_widths[d.id] / 2) &&
        (x > d.x - net_widths[d.id] / 2) &&
        (y < d.y + net_heights[d.id] / 2) &&
        (y > d.y - net_heights[d.id] / 2);
}

//Check if node, n is close to origin object, o
function close_to(n, o) { //n is node, o is origin
    if (o.type == "net") { //if origin is net
        if (!(n.type == "net")) { //if node is nde or ens
            if (!netContains(n, o)) {
                if (Math.abs(o.x - n.x) < (net_margin + net_widths[o.id] / 2) &&
                    Math.abs(o.y - n.y) < (net_margin + net_heights[o.id] / 2)) {
                    //console.log('true 1')
                    return true
                }
            }
        } else if (!(netContains(n, o) || netContains(o, n))) { //if node is net
            if (Math.abs(o.x - n.x) < (net_widths[n.id] / 2 
                + net_widths[o.id] / 2) && Math.abs(o.y - n.y) < 
                (net_heights[n.id] / 2 + net_heights[o.id] / 2)) {
                //console.log('true 2')
                return true
            }
        }
    } else { //if origin is nde or ens
        if (!(n.type == "net")) { //if node nde or ens
            if (Math.abs(o.x - n.x) < node_margin && Math.abs(o.y - n.y) < node_margin) {
                //console.log('true 3')
                return true
            }
        } else { //if node is net
            if (!netContains(o, n)) {
                if (Math.abs(o.x - n.x) < (net_margin + net_widths[n.id] / 2) &&
                    Math.abs(o.y - n.y) < (net_margin + net_heights[n.id] / 2)) {
                    //console.log('true 4')
                    return true
                }
            }
        }
    }
    return false
}

//True if net or any of its subnets contains node
function netContains(node, net) {
    ind = graph.nodes.indexOf(node)
    if (net.full_contains.indexOf(ind) > -1) {
        return true
    } else {
        return false
    }
}

//Comparing full_contains length if it exists, for sorting
function containsCompare(a,b) {
    if (a.type!='net') {
        return 1;
    } else if (b.type != 'net') {
        return -1;
    } else if (b.type!='net' && a.type!='net') {
        return 0;
    } else {
        return b.full_contains.length-a.full_contains.length;
    }
}

//*****************
// Reload the graph
//*****************
var graph = null;
var link = null;
var linkRecur = null;
var nodes = null;
var nets = null;
var node_margin = 35;
var net_inner_margin = 40;
var net_margin = 15;
var node_fontsize = 16;

var waiting_for_result = false;
var pending_change = false;
function reload_graph_data() {
    // don't send a new request while we're still waiting for another one
    if (waiting_for_result) {
        pending_change = true;
        return;
    }
    
    waiting_for_result = true;
    
    var data = new FormData();
    data.append('code', editor.getValue());

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/graph.json', true);
    xhr.onload = update_graph;
    xhr.send(data);
}

//Redraw the graph given server response
function update_graph() {
    waiting_for_result = false;
    
    if (pending_change) {
        pending_change = false;
        reload_graph_data();
    }
    
	graph = JSON.parse(this.responseText);

    // was there a parsing error?
    if (graph.error_line != undefined) {
        removeMarker();
        marker = editor.getSession()
            .addMarker(new aceRange(graph.error_line - 1, 0, graph.error_line - 1, 10), 
            'highlight', 'fullLine', true);
        editor.getSession().setAnnotations([{
            row: graph.error_line - 1,
            type: 'error'
        }]);
        return;
    } else {
        if (marker != null) {
            editor.getSession().removeMarker(marker);
            marker = null;
        }
        editor.getSession().clearAnnotations();
    }

    //separate links into recurrent and nonrecurrent ?move to convert?  
    var nonrecurlink = []
    var recurlink = []
    for (i in graph.links) {
        if (graph.links[i].target != graph.links[i].source) {
            nonrecurlink.push(graph.links[i])
        } else {
            recurlink.push(graph.links[i])
        }
    }

    //update the links
    link = container.selectAll('.link.link_std, .link.link_net')
        .data(nonrecurlink, function (d) {return d.id})
    link.enter().append('polyline')
        .attr('class', function (d) {return 'link link_' + d.type;})

    linkRecur = container.selectAll('.link.link_recur')
        .data(recurlink, function (d) {return d.id})
    linkRecur.enter().append('use')
        .attr('class', function (d) {return 'link link_recur';})
        .attr('xlink:href', "#recur")
    
    var modelNodes = []
    for (i in graph.nodes) {
        if (graph.nodes[i].type=='mod') {
            for (j in graph.nodes[i].contains) {
                thisNode = graph.nodes[graph.nodes[i].contains[j]];
                if (thisNode.type != 'net') {
                    modelNodes.push(thisNode)
                }
            }
            break; 
        }
    }
        
    var top_nodes = container.selectAll('.node_ens, .node_nde')
        .data(modelNodes, function (d) {return d.id})
    
    top_nodes.enter()
        .append('g')
        .attr('class', function (d) {return 'node node_' + d.type;})
        .on('mouseover', annotateLine)
        .on('mouseout', clearAnnotation)
        .call(drag); 
        
    nets = container.selectAll('.node_net')
        .data(function (d) {
            thisNodes=[]
            for (i in graph.nodes) {
                if (graph.nodes[i].type=='net') {
                    thisNodes.push(graph.nodes[i]);
                }
            }
            return thisNodes;
        }, 
        function (d) {return d.id})
        
    nets.enter()
        .append('g')
        .attr('class', function (d) {return 'node node_' + d.type;})
        .call(d3.behavior.zoom()
            .scaleExtent([.05, 10])
            .on('zoom', zoomed))
        .on('mouseover', annotateLine)
        .on('mouseout', clearAnnotation)
        .call(drag); 
                   
    subNodes = nets.selectAll('.node_ens, .node_nde')
        .data(function (d) {
            thisNodes=[]
            for (i in d.contains) {
                thisNode = graph.nodes[d.contains[i]];
                thisNodes.push(thisNode)
            }
            return thisNodes 
        },
        function (d) {return d.id})
        
    subNodes.enter()
        .append('g')
        .attr('class', function (d) {return 'node node_' + d.type;})
        .on('mouseover', annotateLine)
        .on('mouseout', clearAnnotation)
        .call(drag);        

    nodes = container.selectAll('.node')

    nodes.filter(function (d) {return d.type == 'ens';})
        .append('use')
        .attr('xlink:href', "#ensemble")
        
    nodes.filter(function (d) {return d.type == 'nde';})
        .append('circle')
        .attr('r', '20')
    
    //container.selectAll('g.node text')
    //    .data(graph.nodes, function (d) {return d.id})

    //Create html objects to draw
    nets.append('rect')
        .attr('x', '-50')
        .attr('y', '-50')
        .attr('rx', '15')
        .attr('ry', '15')
        .attr('width', '100')
        .attr('height', '100')
        
    //label everything
    container.selectAll('.node').append('text')
        .text(function (d) {return d.label})

    container.selectAll('.node_nde text, .node_ens text')
        .attr('y', '30')
        .style('font-size', node_fontsize)

    //draw everything
    container.selectAll('.node')
        .attr('transform', function (d) { return 'translate(' + [d.x, d.y] + ')'})

    subNodes.exit().remove();
    top_nodes.exit().remove();
    nets.exit().remove();
    link.exit().remove();
    linkRecur.exit().remove();

    layer_container(); //redraw so nodes are on top, lowest level nets 2nd, and so on

    for (i in graph.nodes) { //set up all network sizes
        update_net_size(graph.nodes[i], 0, 0);
    }
    update_line_locations();
    resize();
}

//***********
//Main script
//***********
$(document).ready(function () {
    zoom = d3.behavior.zoom()
        .scaleExtent([.05, 10])
        .on('zoom', zoomed);

    drag = d3.behavior.drag()
        .origin(function (d) {return d})
        .on('dragstart', dragstarted)
        .on('drag', dragged)
        .on('dragend', dragended);

    //initialize editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.on('change', function(event) {if (!gui_updating) reload_graph_data();});

    //initialize file browser
    $('#filebrowser').hide()
    $('#menu_open').click(function () {
        $('#filebrowser').toggle(200);
    })
    $('#filebrowser').fileTree({
        root: '.',
        script: '/browse'
    }, open_file);

    //initialize graph
    svg = d3.select("svg");
    container = svg.append('g');
    svg.call(zoom); // set up zooming on the graph
    
    d3.select(window).on("resize", resize);

    //start this puppy up
    reload_graph_data();
});