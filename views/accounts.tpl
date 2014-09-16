% include('header.tpl')
        <li><a href="/">Home</a></li>
        <li><a href="/getting_started">Getting Started</a></li>
        <li class="active"><a href="/accounts">Accounts</a></li>
        <li><a href="/blocks">Blocks</a></li>
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
<h1>Active Accounts List:</h1>
</div>
<div class="table-responsive">
<div id="loctable"></div>
<script>
$.getJSON("/api/accounts", function(data) {
    $("#loctable").mrjsontable({
        tableClass: "my-table table-striped table-bordered table-condensed table-hover",
        pageSize: 10, //you can change the page size here
        columns: [
            new $.fn.mrjsontablecolumn({
                heading: "Account",
                data: "ars"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Height From",
                data: "heightfrom"
            }),
            new $.fn.mrjsontablecolumn({
                heading: "Height To",
                data: "heightto"
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
% include('footer.tpl')
