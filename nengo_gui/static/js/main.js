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

function update_gui_text() {
    gui_updating = true;
    var gui = '\n\nimport nengo_gui\ngui = nengo_gui.Config()\n';
    gui += "gui[model].scale = " + ModelVisGui.zoom.scale() + "\n";
    gui += "gui[model].offset = " + ModelVisGui.zoom.translate() + "\n";
    for (var i=0; i<graph.nodes.length; i++) {
        d = graph.nodes[i];
        if ((d.type == 'ens') || (d.type == 'nde')) {
            gui += "gui[" + d.id + "].pos = " + 
                            d.x.toFixed(3) + ", " + d.y.toFixed(3) + "\n";
            gui += "gui[" + d.id + "].scale = " + d.scale.toFixed(3) + "\n";
        }
        if (d.type == "net") {
            gui += "gui[" + d.id + "].pos = " + 
                            d.x.toFixed(3) + ", " + d.y.toFixed(3) + "\n";
            gui += "gui[" + d.id + "].scale = " + d.scale.toFixed(3) + "\n";
            gui += "gui[" + d.id + "].size = " + 
                            d.width.toFixed(3) + ", " + d.height.toFixed(3) + "\n";
        }
    }
    
    text = editor.getValue();
    index = text.indexOf('\n\nimport nengo_gui\n');
    if (index!=-1) {
        text = text.substring(0, index);
    } else {
        // also check if line endings changed on us
        index = text.indexOf('\r\n\r\nimport nengo_gui\r\n');
        if (index!=-1) {
            text = text.substring(0, index);
        }
    }
    
    new_text = text + gui;
    
    cursor = editor.getCursorPosition();
    scroll_top = editor.session.getScrollTop();
    scroll_left = editor.session.getScrollLeft();
    editor.session.setValue(new_text);
    editor.moveCursorToPosition(cursor);
    editor.session.setScrollTop(scroll_top);
    editor.session.setScrollLeft(scroll_left);
    gui_updating = false;    
}
//*****************
// Helper functions
//*****************
var ModelVisGui = Object.create(ModelVis);
//**************
// Drag and zoom
//**************

ModelVisGui.dragged = function(mv, d) {
    ModelVis.dragged.call(this, mv, d);
    update_gui_text();
};

ModelVisGui.zoomed = function(mv, node) {
    ModelVis.zoomed.call(this, mv, node);
    update_gui_text();
};

ModelVisGui.zoomCenter = function(d) { //zoom full screen and center the network clicked on
    var zoomNet = d
    
    if (d3.event !== null) {
        try {d3.event.stopPropagation();}
        catch (e) {if (e instanceof TypeError) {
            console.log('ZoomCenter Ignored Error: ' + e)
        }}
    }
    
    if (d == undefined) { //background click
        zoomNet = -1
    } else if (d.type !== 'net') { //if node or ens
         if (d.contained_by == -1) { //background click
            zoomNet = -1 
         } else { //use containing network
            zoomNet = graph.nodes[d.contained_by]
        }
    }

    var width = nengoLayout.center.state.innerWidth;
    var height = nengoLayout.center.state.innerHeight;

    if (zoomNet == -1) { //zoom out to full model
        var netWidth = d3.select('#modelGroup').node()
            .getBBox().width;
        var netHeight = d3.select('#modelGroup').node()
            .getBBox().height;

    } else { //zoom to fit zoomNet
        var netWidth = zoomNet.width*zoomNet.scale
        var netHeight = zoomNet.height*zoomNet.scale
        var netX = zoomNet.x
        var netY = zoomNet.y
    }
    
    if (width/height >= netWidth/netHeight) {
        //zoom to height
        scale = .9*height/netHeight
    } else {
        //zoom to width
        scale = .9*width/netWidth
    }

    console.log(scale);
    if (isNaN(scale)) {
        scale = 1.0;
    } 
    
    if (scale == Infinity) {
        scale = 1.0;
    }

    this.zoom.scale(scale)
    
    if (zoomNet == -1) {
        var netX = d3.select('#modelGroup').node().getBBox().x;
        var netY = d3.select('#modelGroup').node().getBBox().y

        this.zoom.translate([width/2 - (netWidth/2 + netX)*scale,
            height/2 - (netHeight/2 + netY)*scale])            
    } else {
        this.zoom.translate([width/2 - netX*scale, height/2-netY*scale])
    }

    this.zoom.event(this.container.transition().duration(500))
};

/*function parseTranslate(inString) {
    var split = inString.split(",");
    var x = split[0] ? split[0].split("(")[1] : 0;
    var y = split[1] ? split[1].split(")")[0] : 0;
    var s = split[1] ? split[1].split(")")[1].split("(")[1] : null;
    return [x, y, s];
};*/

//***********************
// Drawing graph elements
//***********************
ModelVisGui.waiting_for_result = false;
ModelVisGui.pending_change = false;

ModelVisGui.reload_graph_data = function() {
    // don't send a new request while we're still waiting for another one
    if (this.waiting_for_result) {
        this.pending_change = true;
        return;
    }
    
    this.waiting_for_result = true;
    
    var data = new FormData();
    data.append('code', editor.getValue());

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/graph.json', true);
    var mv = this;
    xhr.onload = function() { mv.update_graph_gui.bind(this)(mv); };
    xhr.send(data);
};

//Redraw the graph given server response
ModelVisGui.update_graph_gui = function(mv) {
    mv.waiting_for_result = false;
    
    if (mv.pending_change) {
        mv.pending_change = false;
        mv.reload_graph_data();
    }
    
	graph2 = JSON.parse(this.responseText);

    // was there a parsing error?
    if (graph2.error_line != undefined) {
        removeMarker();
        marker = editor.getSession()
            .addMarker(new aceRange(graph2.error_line - 1, 0, graph2.error_line - 1, 10), 
            'highlight', 'fullLine', true);
        editor.getSession().setAnnotations([{
            row: graph2.error_line - 1,
            type: 'error',
            text: graph2.text,
        }]);
        return;
    } else {
        graph = graph2
        if (marker != null) {
            editor.getSession().removeMarker(marker);
            marker = null;
        }
        editor.getSession().clearAnnotations();
    }

    mv.update_graph(graph);
};

//***********
//Main script
//***********
$(document).ready(function () {
    //initialize editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setUseSoftTabs(true);
    editor.getSession().setMode("ace/mode/python");
    editor.on('change', function(event) {
        $('#menu_save').removeClass('disable');
        if (!gui_updating) ModelVisGui.reload_graph_data();
    });

    //setup the window panes, and manipulations
    nengoLayout = $('body').layout({ 
	    north__slidable:			false,	
		north__resizsable:			false,	
		north__spacing_open:        0,
		north__size:                55, //pixels
		east__livePaneResizing:		true,
		east__size:					.4,
		east__minSize:				.1,
		east__maxSize:				.8, // 80% of layout width 
		east__onresize:             function() {editor.resize(true)}       
    });

    ModelVisGui.common_init();
    //start this puppy up
    ModelVisGui.reload_graph_data();
});
