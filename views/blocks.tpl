% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li class="active"><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>
  
<div class="container">
  
  <div class="text-center">
  	<div class="page-header">
	<h1>Block List:</h1>
  	</div>
	<div class="col-lg-12">
	<h3>Estimated Time</h3>    
    <p><div id="btime"></div></p>
	</div>
	<script>
  $.getJSON('/api/btime', function(data) {
        var output="<p><strong>Until Next Block: </strong>" + data.blocktime + "</p>";
        document.getElementById("btime").innerHTML=output;
  });
    </script>
<div class="table-responsive">
<div id="loctable"></div>
<script>
$.getJSON("/api/blocks", function(data) {
    $("#loctable").mrjsontable({
        tableClass: "my-table table-striped table-bordered table-condensed table-hover",
        pageSize: 10, //you can change the page size here
        columns: [
            new $.fn.mrjsontablecolumn({
                heading: "Timestamp",
                data: "timestamp"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Height",
                data: "height"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Total Fee",
                data: "totalfee"
            })
        ],
        data: data
    });
});
</script>
</div>
</div>  
</div>
</div>
% include('footer.tpl')