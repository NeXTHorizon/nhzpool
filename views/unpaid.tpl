% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/getting_started">Getting Started</a></li>
        <li><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
        <li><a href="/payouts">Payouts</a></li>
		<li class="active"><a href="/unpaid">Unpaid</a></li>
		<li><a href="/paid">Paid</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>

<div class="container">
  
  <div class="text-center">
	<div class="page-header">
		<h1>Unpaid Transactions:</h1>
	</div>
</div>
<div class="table-responsive">
<div id="loctable"></div>
<script>
$.getJSON("/api/unpaid", function(data) {
    $("#loctable").mrjsontable({
        tableClass: "my-table table-striped table-bordered table-condensed table-hover",
        pageSize: 10, //you can change the page size here
        columns: [
            new $.fn.mrjsontablecolumn({
                heading: "Blocktime",
                data: "blocktime"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Account",
                data: "account"
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
% include('footer.tpl')
