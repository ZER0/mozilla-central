// |jit-test| error: ExitCleanly

// proxies can return primitives
assertEq(new (Proxy.createFunction({}, function(){}, function(){})), undefined);
x = Proxy.createFunction((function () {}), Uint16Array, wrap)
new(wrap(x))
// proxies can return the callee
var x = Proxy.createFunction({}, function (q) { return q; });
assertEq(new x(x), x);
try {
    var x = (Proxy.createFunction({}, "".indexOf));
    new x;
}
catch (e) {
    assertEq(e.message, 'new x is not a constructor');
}
throw "ExitCleanly"
