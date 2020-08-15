console.log("heloo there");


var pathname = window.location.pathname;
var potato_id = window.location.pathname.split("/").pop();

console.log(pathname);
// console.log(pathname2);

// specify the columns
$(document).ready(function() {
    $.getJSON(pathname).done(function (data) {
        console.log(data);
        $("#name").text(data.name);
        var columnDefs = [" "].concat(data.table.users).map(function(user){
            if (user === " "){
                return {headerName: user, field: user,  editable:true }
            } else {
                return {headerName: user, field: user, editable:true, valueParser: numberParser}
            }
        });

        //adding click me buttons
        // columnDefs.push({headerName: ({cellRenderer: "btnCellRenderer"}), field: "blob",  editable:true, 
        //     cellRenderer: "btnCellRenderer", 
        //     cellRendererParams:{ clicked : function(field){
        //         alert("was clicked");
        //     }}})

        function numberParser(params) {
            return Number(params.newValue);
        }

        var choices = data.table.choices;
        var rowData=[];
        
        for (var key in choices){ 
            userDict = (choices[key]);
            userDict[" "]=key;
            rowData.push(userDict);
        };

        //********autosizing table */
        var gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,
    
        onFirstDataRendered: onFirstDataRendered,
        onGridSizeChanged: onGridSizeChanged,
        onCellValueChanged: function(event) {
            $.post(pathname + "/weight",{user: event.colDef.field , option: event.data[" "] , weight: event.newValue})
            console.log('data after changes is: ', event.colDef.field, event.data[" "], event.newValue);
          },
        components: { btnCellRenderer: BtnCellRenderer},
        // enableCellTextSelection=true
        };

        function onFirstDataRendered(params) {
            params.api.sizeColumnsToFit();
        };

        function onGridSizeChanged(params) {
            // get the current grids width
            var gridWidth = document.getElementById('grid-wrapper').offsetWidth;
          
            // keep track of which columns to hide/show
            var columnsToShow = [];
            var columnsToHide = [];
          
            // iterate over all columns (visible or not) and work out
            // now many columns can fit (based on their minWidth)
            var totalColsWidth = 0;
            var allColumns = params.columnApi.getAllColumns();
            for (var i = 0; i < allColumns.length; i++) {
              var column = allColumns[i];
              totalColsWidth += column.getMinWidth();
              if (totalColsWidth > gridWidth) {
                columnsToHide.push(column.colId);
              } else {
                columnsToShow.push(column.colId);
              }
            }
          
            // show/hide columns based on current grid width
            params.columnApi.setColumnsVisible(columnsToShow, true);
            params.columnApi.setColumnsVisible(columnsToHide, false);
          
            // fill out any available space to ensure there are no gaps
            params.api.sizeColumnsToFit();
        };

        function BtnCellRenderer() {}
        BtnCellRenderer.prototype.init = function(params) {
            this.params = params;
          
            this.eGui = document.createElement('button');
            this.eGui.innerHTML = 'Click me!';
          
            this.btnClickedHandler = this.btnClickedHandler.bind(this);
            this.eGui.addEventListener('click', this.btnClickedHandler);
        }
        
        BtnCellRenderer.prototype.getGui = function() {
            return this.eGui;
        }

        BtnCellRenderer.prototype.destroy = function() {
            this.eGui.removeEventListener('click', this.btnClickedHandler);
        }
        
         BtnCellRenderer.prototype.btnClickedHandler = function(event) {
           this.params.clicked(this.params.value);
        }

        var eGridDiv = document.querySelector('#myGrid');
        var newGrid = new agGrid.Grid(eGridDiv, gridOptions);

        function addUser() {
            columnDefs.push({headerName :"new user", field : "new user"});
            $("#myGrid").empty();
            var grid = new agGrid.Grid(eGridDiv, gridOptions);                
        }

        function addOption(){
            rowData.push({" ":"new option"})
            $("#myGrid").empty();
            var grid = new agGrid.Grid(eGridDiv, gridOptions);
        }

        $("#add-user").click(addUser);
        $("#add-option").click(addOption);

    });
});

// var columnDefs = [
//     {headerName: "Make", field: "make"},
//     {headerName: "Model", field: "model"},
//     {headerName: "Price", field: "price"}
//   ];

// //   specify the data
//   var rowData = [
//     {make: "Toyota", model: "Celica", price: 35000},
//     {make: "Ford", model: "Mondeo", price: 32000},
//     {make: "Porsche", model: "Boxter", price: 72000}
//   ];

//   // let the grid know which columns and what data to use
//   var gridOptions = {
//     columnDefs: columnDefs,
//     rowData: rowData
//   };

// // lookup the container we want the Grid to use
// var eGridDiv = document.querySelector('#myGrid');

// // create the grid passing in the div to use together with the columns & data we want to use
// new agGrid.Grid(eGridDiv, gridOptions);
