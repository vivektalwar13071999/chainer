import chainer
from chainer import functions as F
import numpy

import chainerx

from chainerx_tests import dtype_utils
from chainerx_tests import op_utils


_in_out_loss_dtypes = dtype_utils._permutate_dtype_mapping([
    (('float16', 'float16'), 'float16'),
    (('float32', 'float32'), 'float32'),
    (('float64', 'float64'), 'float64'),
    (('float32', 'float16'), 'float32'),
    (('float64', 'float16'), 'float64'),
    (('float64', 'float32'), 'float64'),
])


class LossBase(op_utils.ChainerOpTest):

    def generate_inputs(self):
        y = numpy.random.normal(loc=0, scale=3.0, size=self.shape)
        targ = numpy.random.normal(loc=0, scale=2.0, size=self.shape) + \
            numpy.random.uniform(0, 1, size=self.shape)
        return y, targ

    def forward_chainerx(self, inputs):
        return self.forward_xp(inputs, chainerx)

    def forward_chainer(self, inputs):
        return self.forward_xp(inputs, F)

    def forward_xp(self, inputs, xp):
        raise NotImplementedError(
            'Op test implementation must override `forward_xp`.')


@op_utils.op_test(['native:0', 'cuda:0'])
@chainer.testing.parameterize(*(
    chainer.testing.product([
        chainer.testing.from_pytest_parameterize(
            'shape', [
                (2, 2),
                (3, 3, 3),
                (5, 5, 5),
                (4, 1, 2, 4)
            ]),
        chainer.testing.from_pytest_parameterize(
            'in_dtypes,out_dtype', _in_out_loss_dtypes)
    ])
))
class TestMSE(LossBase):

    def forward_xp(self, inputs, xp):
        x0, x1 = inputs
        return xp.mean_squared_error(x0, x1),


@op_utils.op_test(['native:0', 'cuda:0'])
@chainer.testing.parameterize(*(
    chainer.testing.product([
        chainer.testing.from_pytest_parameterize(
            'shape', [
                (2, 2),
                (3, 3, 3),
                (5, 5, 5),
                (4, 1, 2, 4)
            ]),
        chainer.testing.from_pytest_parameterize(
            'in_dtypes,out_dtype', _in_out_loss_dtypes)
    ])
))
class TestMAE(LossBase):

    def forward_xp(self, inputs, xp):
        x0, x1 = inputs
        return xp.mean_absolute_error(x0, x1),


@op_utils.op_test(['native:0', 'cuda:0'])
@chainer.testing.parameterize(*(
    chainer.testing.product([
        chainer.testing.from_pytest_parameterize(
            'shape', [
                (2, 2),
                (3, 3, 3),
                (5, 5, 5),
                (4, 1, 2, 4)
            ]),
        chainer.testing.from_pytest_parameterize(
            'in_dtypes,out_dtype', _in_out_loss_dtypes),
        chainer.testing.from_pytest_parameterize(
            'reduce', ['sum', 'mean'])
    ])
))
class TestGaussianKLDivergence(LossBase):

    def forward_xp(self, inputs, xp):
        mean, ln_var = inputs
        return xp.gaussian_kl_divergence(mean, ln_var, reduce=self.reduce),
