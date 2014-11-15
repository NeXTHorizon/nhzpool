% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/getting_started">Getting Started</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li><a href="/unpaid">Unpaid</a></li>
		<li class="active"><a href="/paid">Paid</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>

<div class="container">
  
  <div class="text-center">
	<div class="page-header">
		<h1>{{aid}}<p><small>{{user}}</small></p></h1>
	</div>

<div class="row">
  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
  <h3>Paid</h3>
  <div class="table-responsive">
<div id="paid"></div>
<script>
$.getJSON("/api/userpaid/{{user}}", function(data) {
    $("#paid").mrjsontable({
        tableClass: "my-table table-striped table-bordered table-condensed table-hover",
        pageSize: 10, //you can change the page size here
        columns: [
            new $.fn.mrjsontablecolumn({
                heading: "Blocktime",
                data: "blocktime"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Percentage",
                data: "percentage"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Amount",
                data: "amount"
            })
        ],
        data: data
    });
});
</script>
</div>
  </div>
  <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
  <h3>Unpaid</h3>
    <div class="table-responsive">
<div id="unpaid"></div>
<script>
$.getJSON("/api/userunpaid/{{user}}", function(data) {
    $("#unpaid").mrjsontable({
        tableClass: "my-table table-striped table-bordered table-condensed table-hover",
        pageSize: 10, //you can change the page size here
        columns: [
            new $.fn.mrjsontablecolumn({
                heading: "Blocktime",
                data: "blocktime"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Percentage",
                data: "percentage"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Amount",
                data: "amount"
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
</div>
</div>
% include('footer.tpl')
